import cv2
from TestFaceRecognizer import FaceRecognizer

if __name__ == '__main__':

    video_capture = cv2.VideoCapture(0)
    facerecognizer = FaceRecognizer()
    for i in range(300):
        ret, frame = video_capture.read()
        facerecognizer.run(frame)
