
import cv2
import math
import numpy as np
import os
import time
import h5py

intial_time = str(math.floor(time.time()))

path = '/home/pi/.virtualenvs/cv_wh/ProjectDocs/code/miniprojectData/' + intial_time + '/'

if not os.path.exists(path):
    os.makedirs(path)

filename = str(math.floor(time.time())) + '.avi'

cap = cv2.VideoCapture(0)
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter(path + filename,fourcc,fps=1,frameSize=(640,480))

car_cascade = cv2.CascadeClassifier('cars.xml')

count=0
i = 0;
carcount_arr = np.zeros(20);

tstop = time.time() + 20
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
    cv2.imshow('frame',frame)
    
    i +=1

    carcount_arr[i]=len(cars)
    #print (frame.shape)
    print ("number of cars:" )
    print (carcount_arr[i])



        
    key = cv2.waitKey(1)
    #print (key)
    # If 'q' key was pressed, exit the loop (q == 113 in binary)
    # Note that the video frame must be selected for this to work.
    # If cv2.imshow('frame',frame) is not include the file will be output but 'q' will not exit the loop 
    if key == 113:
        break

with h5py.File('testfile.hdf5','w') as f:
    dset = f.create_dataset('carcount', data=carcount_arr)
dset.name   
    #f.create_dataset('time',data=time.time())
    
    
##with h5py.File('testfile.hdf5','r') as f:
##    data = f.get('carcount')
##    carcount = np.array(data)
##    ls = list(f.keys())
##    print(ls)
##    print(carcount.shape)
##    carcount[0]
##    
cap.release()
out.release()
cv2.destroyAllWindows()

