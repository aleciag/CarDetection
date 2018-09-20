
# Adapted from https://tutorial.cytron.io/2017/08/16/raspberry-pi-zero-w-pi-camera-application/


from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import imutils

faceCascade = cv2.CascadeClassifier('/home/pi/.virtualenvs/cv_wh/lib/haarcascades/haarcascade_frontalface_alt.xml')

camera = PiCamera()
camera.resolution = (240, 240)
camera.framerate = 24

rawCapture = PiRGBArray(camera, size=(240, 240))

# allow the camera to warmup
time.sleep(0.1)

# capture frames from the camera
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    image = frame.array
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    #Detect faces in the image
    faces = faceCascade.detectMultiScale(gray, 1.3, 5)
    print(" Found {0} faces!".format(len(faces)))
    
    
    # Draw circle around the face
    for (x, y, w, h) in faces:
        cv2.circle(image, (int(x+w/2), int(y+h/2)), int((w+h)/3), (255, 255, 255), 1)
        
       

    # show the frame
    cv2.imshow("Frame", image)
    key = cv2.waitKey(1) & 0xFF
    # clear the stream in preparation for the next frame
    rawCapture.truncate(0)
    # if the 'q' key was pressed, break from the loop
    if key == ord("q"):
        break
