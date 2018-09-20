#
# Final version of our live car counting script.
#
# Created by Zachary Safran and Alecia Griffin.
#
import cv2
import math
import numpy as np
import os
import time
import h5py

# time.time() from the time library returns the current Epoch time
# This was used inconjunction with the os library to create unique files
# and directories each time the sript is run.
start_time = str(math.floor(time.time()))
start_path = '/home/pi/.virtualenvs/cv_wh/ProjectDocs/code/miniprojectData/' + start_time + '/'

# Makes a new directory when the script starts at boot up
if not os.path.exists(start_path):
    os.makedirs(start_path)

# Changes paths to the newly created directory
os.chdir( start_path )

# Next the program runs in a continues loop capturing and processing ~5 mins of video
# At the end of each loop a .avi video file and a .hdf5 data file are output.
# This loop will run until the Pi is powered off or the program is killed by the user.
while True:
    record_time = str(math.floor(time.time()))

    path = start_path + record_time + '/'

    # A new folder is created to contain the files output by a given "loop cycle"
    if not os.path.exists(path):
        os.makedirs(path)

    os.chdir( path )

    filename = str(math.floor(time.time())) + '.avi'

    # Video starts being captured and output .avi file is set up.
    cap = cv2.VideoCapture(0)
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(path + filename,fourcc,fps=1,frameSize=(640,480))

    # CascadeClassifier is set up to detect cars with the cars.xml classifier
    car_cascade = cv2.CascadeClassifier('/home/pi/.virtualenvs/cv_wh/ProjectDocs/code/Car Detection/cars.xml')

    count=0
    i = 0

    # Arrays for data are preallocated.
    carcount_arr = np.zeros(240)
    time_arr = np.zeros(240)

    tstop = time.time() + 310
    # Video is set to record for ~5mins.
    while time.time() < tstop:

        # Each frame is captured individually.
        ret,frame=cap.read()
        # Convert video into gray scale of each frames.
        gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        # Each frame is analyzed for cars.
        cars = car_cascade.detectMultiScale(gray, 1.3, 5)
        for (x,y,w,h) in cars:
            # A BLUE rectangle is placed around the detected cars and the variable count is incremented.
            cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
            roi_color = frame[y:y+h, x:x+w]
            count+=1

        # Text of the cummulative car count is added to each frame.
        cv2.putText(frame, str(count),(10,400), cv2.FONT_ITALIC, 2,(255,255,255),2,cv2.LINE_AA)
        # The frame is written to the .avi output file.
        out.write(frame)
        # The following line is commented out to allow this sript to run without a display
        # cv2.imshow('frame',frame)

        if i < 240:
            # For 240 iterations the time and number of cars detected in each frame are stored in the data arrays.
            time_arr[i] = time.time()
            carcount_arr[i]=len(cars)
            print ("number of cars:" )
            print (carcount_arr[i])
            i += 1

    # After ~5 mins the loop exits and a unique .hdf5 file is created.
    datafile = str(math.floor(time.time())) + '.hdf5'
    with h5py.File(datafile,'w') as f:
        # The data arrays containing the cars per frame and time of each frame are written into the .hdf5 file
        f.create_dataset('carcount', data=carcount_arr)
        f.create_dataset('time', data=time_arr)

    # This file was then read from and printed so that the user could verify that the data was recorded and output correctly.
    f = h5py.File(datafile,'r')
    getcardata = f['carcount'].value
    gettimedata = f['time'].value
    print(getcardata)
    print(gettimedata)


    # Release the videocapture object and file
    cap.release()
    out.release()
    # Close all of the frames.
    cv2.destroyAllWindows()
