import cv2
from TestFaceRecognizer import FaceRecognizer
import time
import matplotlib.pyplot as plt
import numpy as np


def getNearestValue(list, num):
    idx = np.abs(np.asarray(list) - num).argmin()
    return idx


def plot(X, Y, offset, targetvalue, filename):
    Y10percent = Y[getNearestValue(Y, max(Y)*0.1)]
    Y90percent = Y[getNearestValue(Y, max(Y)*0.9)]
    Y98percent = Y[getNearestValue(Y, max(Y)*0.98)]
    X2percent = X[getNearestValue(Y, max(Y)*0.02)]
    X10percent = X[getNearestValue(Y, max(Y)*0.1)]
    X90percent = X[getNearestValue(Y, max(Y)*0.9)]
    X98percent = X[getNearestValue(Y, max(Y)*0.98)]

    plt.ylim(0, 400)
    plt.xlabel('Times(s)')
    plt.ylabel('pixels of frame')
    plt.axhline(y=Y10percent, xmin=0, xmax=1)
    plt.axhline(y=Y90percent, xmin=0, xmax=1)
    plt.axhline(y=Y98percent, xmin=0, xmax=1)
    plt.axvline(x=X2percent, ymin=0, ymax=1, c='orange')
    plt.axvline(x=X10percent, ymin=0, ymax=1, c='gray')
    plt.axvline(x=X90percent, ymin=0, ymax=1, c='gray')
    plt.axvline(x=X98percent, ymin=0, ymax=1, c='orange')

    point = {
        'start': [X2percent, 300],
        'end': [X98percent, 300]
    }

    plt.annotate('Settling Time '+str(round(X98percent - X2percent, 2))+' second', xy=point['start'], xytext=point['end'],
                 arrowprops=dict(arrowstyle='<->',
                                 facecolor='orange',
                                 edgecolor='orange')
                 )

    point = {
        'start': [X10percent, 350],
        'end': [X90percent, 350]
    }

    plt.annotate('Rise Time '+str(round(X90percent - X10percent, 2))+' second', xy=point['start'], xytext=point['end'],
                 arrowprops=dict(arrowstyle='<->',
                                 facecolor='gray',
                                 edgecolor='gray')
                 )

    point = {
        'start': [3, targetvalue - offset],
        'end': [3, 350]
    }

    plt.annotate('Target Value', xy=point['start'], xytext=point['end'],
                 arrowprops=dict(arrowstyle='->',
                                 facecolor='C0',
                                 edgecolor='C0')
                 )

    plt.plot(X, Y, "blue")
    plt.savefig(filename)


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

    tunedT = []
    for t in Time:
        tunedT.append(t - min(Time))

    tunedX = []
    for x in X:
        tunedX.append(x - min(X))

    tunedY = []
    for y in Y:
        tunedY.append(y - min(Y))

    targetvalueX = video_capture.get(cv2.CAP_PROP_FRAME_WIDTH) / 2
    targetvalueY = video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT) / 2
    offsetX = min(X)
    offsetY = min(Y)

    plot(tunedT, tunedX, offsetX, targetvalueX, 'StepResponseinXaxis.png')
    #plot(tunedT, tunedY, offsetY, targetvalueY, 'StepResponseinYaxis.png')
