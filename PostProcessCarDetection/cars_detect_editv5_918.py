
import cv2
import math
import numpy as np
import os
import time
import h5py

start_time = str(math.floor(time.time()))
start_path = '/home/pi/.virtualenvs/cv_wh/ProjectDocs/code/miniprojectData/' + start_time + '/'

if not os.path.exists(start_path):
    os.makedirs(start_path)

os.chdir( start_path )

while True:
    record_time = str(math.floor(time.time()))

    path = start_path + record_time + '/'

    if not os.path.exists(path):
        os.makedirs(path)

    os.chdir( path )

    filename = str(math.floor(time.time())) + '.avi'

    cap = cv2.VideoCapture(0)
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(path + filename,fourcc,fps=1,frameSize=(640,480))

    car_cascade = cv2.CascadeClassifier('/home/pi/.virtualenvs/cv_wh/ProjectDocs/code/Car Detection/cars.xml')

    count=0
    i = 0
    carcount_arr = np.zeros(240)
    time_arr = np.zeros(240)

    tstop = time.time() + 310
    while time.time() < tstop:
        
        ret,frame=cap.read()
        gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY) 
        cars = car_cascade.detectMultiScale(gray, 1.3, 5)
        for (x,y,w,h) in cars:
            cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
            roi_color = frame[y:y+h, x:x+w]
            count+=1
        cv2.putText(frame, str(count),(10,400), cv2.FONT_ITALIC, 2,(255,255,255),2,cv2.LINE_AA)
        out.write(frame)
        # The following line is commented out to allow this sript to run without a display
        # cv2.imshow('frame',frame)

        if i < 240:
            time_arr[i] = time.time()
            carcount_arr[i]=len(cars)
            print ("number of cars:" )
            print (carcount_arr[i])
            i += 1
            

    datafile = str(math.floor(time.time())) + '.hdf5'
    with h5py.File(datafile,'w') as f:
        f.create_dataset('carcount', data=carcount_arr)
        f.create_dataset('time', data=time_arr)


    f = h5py.File(datafile,'r')
    getcardata = f['carcount'].value
    gettimedata = f['time'].value
    print(getcardata)
    print(gettimedata)
        
        
           
    cap.release()
    out.release()
    cv2.destroyAllWindows()

