import face_recognition
import cv2
import numpy as np
import socket
import time
import pickle


class FaceRecognizer():
    def __init__(self):
        self.known_face_encodings = []
        self.known_face_names = []

        ip = '192.168.100.134'
        port = 50007
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((ip, port))

        # Initialize some variables
        self.face_locations = []
        self.face_encodings = []
        self.face_names = []

        for i in range(5):
            image = face_recognition.load_image_file(
                "./PictureOfMe/"+str(i)+".jpg")
            face_encoding = face_recognition.face_encodings(image)[0]
            self.known_face_encodings.append(face_encoding)
            self.known_face_names.append(str(i))

    def run(self, frame, t, Time, X, Y):
        # Resize frame of video to 1/4 size for faster face recognition processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = small_frame[:, :, ::-1]

        # Find all the faces and face encodings in the current frame of video
        self.face_locations = face_recognition.face_locations(rgb_small_frame)
        self.face_encodings = face_recognition.face_encodings(
            rgb_small_frame, self.face_locations)

        for face_encoding in self.face_encodings:
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(
                self.known_face_encodings, face_encoding)
            name = "Unknown"

            face_distances = face_recognition.face_distance(
                self.known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = self.known_face_names[best_match_index]

            self.face_names.append(name)

        # Display the results
        for (top, right, bottom, left), name in zip(self.face_locations, self.face_names):
            # Scale back up face locations since the frame we detected in was scaled to 1/4 size
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            X.append(int((left + right) / 2))
            Y.append(int((top + bottom) / 2))
            Time.append(t)

            centerposition = [int((left + right) / 2), int((top + bottom) / 2)]
            centerposition = pickle.dumps(centerposition)
            self.s.sendall(centerposition)
