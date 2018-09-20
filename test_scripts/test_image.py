
# Adapted from https://tutorial.cytron.io/2017/08/16/raspberry-pi-zero-w-pi-camera-application/

from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2

camera = PiCamera()
rawCapture = PiRGBArray(camera)

# lets the camera sensor warm up
time.sleep(0.1)

camera.capture(rawCapture, format="bgr")
image = rawCapture.array

# outputs an image from the NOIR camera
cv2.imshow("Image", image)
cv2.waitKey(0)
