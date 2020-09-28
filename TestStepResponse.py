import cv2
from TestFaceRecognizer import FaceRecognizer
import time
import matplotlib.pyplot as plt
import numpy as np


def getNearestValue(list, num):
    idx = np.abs(np.asarray(list) - num).argmin()
    return idx


if __name__ == '__main__':

    video_capture = cv2.VideoCapture(0)
    facerecognizer = FaceRecognizer()
    X = []
    Y = []
    Time = []
    t = 0
    preT = time.time()

    for i in range(150):
        ret, frame = video_capture.read()
        facerecognizer.run(frame, t, Time, X, Y)
        T = time.time()
        t += T - preT
        preT = T

    plt.ylim(0, 400)

    tunedT = []
    for t in Time:
        tunedT.append(t - min(Time))

    tunedX = []
    for x in X:
        tunedX.append(x - min(X))

    tunedY = []
    for y in Y:
        tunedY.append(y - min(Y))

    X10percent = tunedX[getNearestValue(tunedX, max(tunedX)*0.1)]
    X90percent = tunedX[getNearestValue(tunedX, max(tunedX)*0.9)]
    X98percent = tunedX[getNearestValue(tunedX, max(tunedX)*0.98)]
    T1percent = tunedT[getNearestValue(tunedX, max(tunedX)*0.01)]
    T10percent = tunedT[getNearestValue(tunedX, max(tunedX)*0.1)]
    T90percent = tunedT[getNearestValue(tunedX, max(tunedX)*0.9)]
    T98percent = tunedT[getNearestValue(tunedX, max(tunedX)*0.98)]

    plt.axhline(y=X10percent, xmin=0, xmax=1)
    plt.axhline(y=X90percent, xmin=0, xmax=1)
    plt.axhline(y=X98percent, xmin=0, xmax=1)
    plt.axvline(x=T1percent, ymin=0, ymax=1, c='orange')
    plt.axvline(x=T10percent, ymin=0, ymax=1, c='gray')
    plt.axvline(x=T90percent, ymin=0, ymax=1, c='gray')
    plt.axvline(x=T98percent, ymin=0, ymax=1, c='orange')

    point = {
        'start': [T1percent, 300],
        'end': [T98percent, 300]
    }

    plt.annotate('Settling Time '+str(round(T98percent - T1percent, 2))+' second', xy=point['start'], xytext=point['end'],
                 arrowprops=dict(arrowstyle='<->',
                                 facecolor='orange',
                                 edgecolor='orange')
                 )

    point = {
        'start': [T10percent, 350],
        'end': [T90percent, 350]
    }

    plt.annotate('Rise Time '+str(round(T90percent - T10percent, 2))+' second', xy=point['start'], xytext=point['end'],
                 arrowprops=dict(arrowstyle='<->',
                                 facecolor='gray',
                                 edgecolor='gray')
                 )

    point = {
        'start': [3, max(X) - min(X)],
        'end': [3, 350]
    }

    plt.annotate('Target Value', xy=point['start'], xytext=point['end'],
                 arrowprops=dict(arrowstyle='->',
                                 facecolor='C0',
                                 edgecolor='C0')
                 )

    plt.plot(tunedT, tunedX, "blue")
    plt.savefig("a.png")
