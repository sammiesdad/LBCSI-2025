import cv2
from picamera2 import Picamera2
import numpy as np 
import pickle
import RPi.GPIO as GPIO
from time import sleep

# GPIO setup
relay_pin = [26]
GPIO.setmode(GPIO.BCM)
GPIO.setup(relay_pin, GPIO.OUT)
GPIO.output(relay_pin, 0)

# Load labels
with open('labels', 'rb') as f:
    dicti = pickle.load(f)

# Camera setup with Picamera2
picam2 = Picamera2()
picam2.configure(picam2.preview_configuration(main={"format": "BGR888", "size": (640, 480)}))
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
                GPIO.output(relay_pin, 1)
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                cv2.putText(frame, name + str(conf), (x, y), font, 2, (0, 0 ,255), 2, cv2.LINE_AA)
            else:
                GPIO.output(relay_pin, 0)

        cv2.imshow('frame', frame)
        key = cv2.waitKey(1)

        if key == 27:
            break
finally:
    picam2.stop()
    GPIO.output(relay_pin, 0)
    GPIO.cleanup()
    cv2.destroyAllWindows()
