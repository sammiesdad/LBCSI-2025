import cv2
from picamera2 import Picamera2
import numpy as np 
import pickle
from gpiozero import OutputDevice
from time import sleep

# GPIOZero relay setup (assuming active HIGH relay)
relay = OutputDevice(26, active_high=True, initial_value=False)

# Load labels
with open('labels', 'rb') as f:
    dicti = pickle.load(f)

# Camera setup with Picamera2
picam2 = Picamera2()
config = picam2.create_preview_configuration(main={"format": "BGR888", "size": (640, 480)})
picam2.configure(config)
picam2.start()

# Face detection and recognition setup
faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read("trainer.yml")

font = cv2.FONT_HERSHEY_SIMPLEX

try:
    while True:
        frame = picam2.capture_array()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(gray, scaleFactor=1.5, minNeighbors=5)

        for (x, y, w, h) in faces:
            roiGray = gray[y:y+h, x:x+w]

            id_, conf = recognizer.predict(roiGray)

            name = "Unknown"
            for n, value in dicti.items():
                if value == id_:
                    name = n
                    print(name)
                    break

            if conf <= 70:
                relay.on()
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                cv2.putText(frame, name + str(conf), (x, y), font, 2, (0, 0 ,255), 2, cv2.LINE_AA)
            else:
                relay.off()

        cv2.imshow('frame', frame)
        key = cv2.waitKey(1)

        if key == 27:
            break
finally:
    picam2.stop()
    relay.off()
    cv2.destroyAllWindows()
