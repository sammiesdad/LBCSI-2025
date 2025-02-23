import cv2
import numpy as np
import os
import sys
from picamera2 import Picamera2

# Initialize Picamera2
picam2 = Picamera2()
config = picam2.create_still_configuration(main={'size': (640, 480)})
picam2.configure(config)
picam2.start()

faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

name = input("What's his/her Name? ")
dirName = "./images/" + name
print(dirName)
if not os.path.exists(dirName):
    os.makedirs(dirName)
    print("Directory Created")
else:
    print("Name already exists")
    sys.exit()

count = 1
while count <= 30:
    frame = picam2.capture_array()
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)  # Convert RGB to BGR for OpenCV
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(gray, scaleFactor=1.5, minNeighbors=5)
    
    for (x, y, w, h) in faces:
        roiGray = gray[y:y+h, x:x+w]
        fileName = f"{dirName}/{name}{count}.jpg"
        cv2.imwrite(fileName, roiGray)
        cv2.imshow("face", roiGray)
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        count += 1
    
    cv2.imshow('frame', frame)
    key = cv2.waitKey(1)
    
    if key == 27:  # ESC key
        break

cv2.destroyAllWindows()
picam2.stop()