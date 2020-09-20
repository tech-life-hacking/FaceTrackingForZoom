import cv2
from FaceRecognizer import FaceRecognizer
from PIL import Image
import numpy as np
from subprocess import Popen, PIPE

if __name__ == '__main__':

    video_capture = cv2.VideoCapture(0)
    p = Popen(['ffmpeg', '-y', '-i', '-', '-pix_fmt', 'yuyv422', '-f', 'v4l2', '/dev/video2'], stdin=PIPE)
    facerecognizer = FaceRecognizer()
    while True:
        ret, frame = video_capture.read()
        facerecognizer.run(frame)
        im = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        im = Image.fromarray(np.uint8(im))
        im.save(p.stdin, 'JPEG')
