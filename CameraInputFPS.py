import cv2
from FaceRecognizer import FaceRecognizer
import time
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

if __name__ == '__main__':

    facerecognizer = FaceRecognizer()
    fpssettings = [30, 25, 20, 15, 10]
    fpslists = []

    video_capture = cv2.VideoCapture(0)
    for i in range(300):
        ret, frame = video_capture.read()
        facerecognizer.run(frame)

    video_capture.release()

    for fpssetting in fpssettings:
        video_capture = cv2.VideoCapture(0)
        video_capture.set(cv2.CAP_PROP_FPS, fpssetting)
        preT = time.time()
        fpslist = []
        for i in range(100):
            ret, frame = video_capture.read()
            facerecognizer.run(frame)
            T = time.time()
            fps = 1 / (T - preT)
            preT = T
            fpslist.append(fps)

        fpslists.append(fpslist)
        video_capture.release()

sns.set()
sns.set_style('whitegrid')
sns.set_palette('Set3')

df = pd.DataFrame({
    '30': fpslists[0],
    '25': fpslists[1],
    '20': fpslists[2],
    '15': fpslists[3],
    '10': fpslists[4],
})

df_melt = pd.melt(df)

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
sns.boxplot(x='variable', y='value', data=df_melt, showfliers=False, ax=ax)
sns.stripplot(x='variable', y='value', data=df_melt,
              jitter=True, color='black', ax=ax)
ax.set_xlabel('Settings of Camera FPS')
ax.set_ylabel('Measured FPS of Face recognition')
ax.set_ylim(5, 35)

plt.show()
fig.savefig("CameraFPSvsFaceRecognitionFPS.png")
