import socket
import pigpio
import time
import pickle

def angle2duty(angle):
    return int(95000 / 180 * angle + 72500)

if __name__ == '__main__':

    ip = 'YourRaspberryPiIPaddress'
    port = 50007
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((ip, port))
    s.listen(1)

    pi = pigpio.pi()
    gpio_pinx = 12
    gpio_piny = 13
    pi.set_mode(gpio_pinx, pigpio.OUTPUT)
    pi.set_mode(gpio_piny, pigpio.OUTPUT)

    x = -60
    y = -50
    pi.hardware_PWM(gpio_pinx,50,angle2duty(x))
    pi.hardware_PWM(gpio_piny,50,angle2duty(y))

    Ix = 0
    Iy = 0
    preT = time.time()
    preerrX = 0
    preerrY = 0
    t = 0
    while True:
        conn, addr = s.accept()
        with conn:
            while True:
                # データを受け取る
                datas = conn.recv(1024)
                datas = pickle.loads(datas)
                array = [int(data) for data in datas]

                T = time.time()
                dt = (T - preT)
                preT = T
                t += dt

                Kp = 0.015
                Ki = 0
                Kd = 0

                errX = 320 - array[0]
                errY = 240 - array[1]

                Px = -Kp * errX
                Ix -= Ki * errX * dt
                Dx = -Kd * (errX - preerrX) / dt

                Py = -Kp * errY
                Iy -= Ki * errY * dt
                Dy = -Kd * (errY - preerrY) / dt

                x += Px + Ix + Dx
                pi.hardware_PWM(gpio_pinx,50,angle2duty(x))

                y += Py + Iy + Dy
                pi.hardware_PWM(gpio_piny,50,angle2duty(y))

                preerrX = errX
                preerrY = errY

                if not array:
                    break
        