from picamera2 import Picamera2
import cv2

# Initialize PiCamera2
picam2 = Picamera2()
picam2.preview_configuration.main.size = (1280, 720)  # Adjust resolution as needed
picam2.preview_configuration.main.format = "RGB888"
picam2.preview_configuration.controls.FrameRate = 30  # Adjust frame rate
picam2.configure("preview")

# Start the camera
picam2.start()

while True:
    frame = picam2.capture_array()
    cv2.imshow("PiCamera2 Stream", frame)

    # Exit on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Cleanup
cv2.destroyAllWindows()
picam2.stop()
