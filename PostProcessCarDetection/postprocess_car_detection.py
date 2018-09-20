#
# Final version of our post process car counting script.
#
# Created by Zachary Safran and Alecia Griffin.
#
import cv2
import numpy as np
import h5py
import time
import math

# Create VideoCapture object and read from video file
cap = cv2.VideoCapture('/home/pi/.virtualenvs/cv_wh/ProjectDocs/code/miniprojectData/1537376806/1537376806/1537376806.avi')
# Use trained cars XML classifiers
car_cascade = cv2.CascadeClassifier('cars.xml')

count = 0
# Array for data is preallocated.
post_carcount = np.zeros(240)
i = 0

# Read until video is completed.

while True:
    # Capture frame by frame.
    ret, frame = cap.read()
    # Convert video into gray scale of each frames.
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Each frame is analyzed for cars.
    cars = car_cascade.detectMultiScale(gray, 1.1, 3)

    # A GREEN rectangle is drawn around the detected cars and the variable count is incremented.
    for (x,y,w,h) in cars:
        cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
        roi_color = frame[y:y+h, x:x+w]
        count+=1
        cv2.putText(frame, str(count),(470,400), cv2.FONT_ITALIC, 2,(0,255,0),2,cv2.LINE_AA)
    # Text of the cummulative car count is added to each frame.
    # Video frame is shown.
    cv2.imshow('video', frame)

    if i < 240:
        # For 240 iterations the number of cars detected in each frame are stored in the data array.
        post_carcount[i] =len(cars)
        print ("number of cars:")
        print (post_carcount[i])
        i += 1


    # Press Q on keyboard to exit.
    if cv2.waitKey(25) & 0xFF == ord('q'):
        break
# After ~5 mins the loop exits and a unique .hdf5 file is created.
datafile = str(math.floor(time.time())) + '.hdf5'
with h5py.File(datafile,'w') as f:
        # The data array containing the cars per frame is written into the .hdf5 file
        f.create_dataset('post_carcount', data=post_carcount)


# This file was then read from and printed so that the user could verify that the data was recorded and output correctly.
f = h5py.File(datafile,'r')
getcardata = f['post_carcount'].value
print(getcardata)

# Release the videocapture object.
cap.release()
# Close all of the frames.
cv2.destroyAllWindows()
