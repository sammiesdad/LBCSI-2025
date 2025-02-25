#!/usr/bin/env python3
from picamera2 import Picamera2
from flask import Flask, Response
import cv2

app = Flask(__name__)

# Initialize and configure the camera
picam2 = Picamera2()
# Create a video configuration (you can also try preview_configuration() if needed)
video_config = picam2.create_video_configuration()
picam2.configure(video_config)
picam2.start()

def generate_frames():
    while True:
        # Capture frame as an array
        frame = picam2.capture_array()
        # Encode frame as JPEG
        ret, jpeg = cv2.imencode('.jpg', frame)
        if not ret:
            continue
        # Yield frame in byte format with MJPEG boundaries
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    # Run on all available IP addresses, port 5000
    app.run(host='0.0.0.0', port=5000, debug=False)
