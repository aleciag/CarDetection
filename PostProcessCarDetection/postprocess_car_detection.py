#import libraries of python opencv
import cv2
import numpy as np
import h5py
import time
import math

#create VideoCapture object and read from video file
cap = cv2.VideoCapture('/home/pi/.virtualenvs/cv_wh/ProjectDocs/code/miniprojectData/1537376806/1537376806/1537376806.avi')
#use trained cars XML classifiers
car_cascade = cv2.CascadeClassifier('cars.xml')

count=0
post_carcount = np.zeros(240)
i = 0

#read until video is completed

while True:
    #capture frame by frame
    ret, frame = cap.read()
    #convert video into gray scale of each frames
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    #detect cars in the video
    cars = car_cascade.detectMultiScale(gray, 1.1, 3)

    #to draw arectangle in each cars 
    for (x,y,w,h) in cars:
        cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)      
        roi_color = frame[y:y+h, x:x+w]
        count+=1
        cv2.putText(frame, str(count),(470,400), cv2.FONT_ITALIC, 2,(0,255,0),2,cv2.LINE_AA)
    #display the resulting frame
    cv2.imshow('video', frame)

    if i < 240:
        post_carcount[i] =len(cars)
        print ("number of cars:")
        print (post_carcount[i]) 
        i += 1
        
    
    #press Q on keyboard to exit
    if cv2.waitKey(25) & 0xFF == ord('q'):
        break

datafile = str(math.floor(time.time())) + '.hdf5'
with h5py.File(datafile,'w') as f:
        f.create_dataset('post_carcount', data=post_carcount)
        


f = h5py.File(datafile,'r')
getcardata = f['post_carcount'].value
print(getcardata)

#release the videocapture object
cap.release()
#close all the frames
cv2.destroyAllWindows()
