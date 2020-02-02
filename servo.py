import numpy as np
import cv2
import RPi.GPIO as GPIO
from picamera import PiCamera
import time

import math
from gpiozero import Servo
from time import sleep
#from video import create_capture
#from common import clock, draw_str

p1=Servo(2) #left
q1=Servo(3) #right
p1.mid()
q1.mid()


cap = cv2.VideoCapture(0)
#print(type(cap))
cap.set(3,320)
cap.set(4,240)
cap.set(5,15)
ret, frame = cap.read()
cv2.namedWindow('frame',cv2.WINDOW_NORMAL)
theta=0
minLineLength = 5
maxLineGap = 10
while(cap.isOpened()):
    # Capture frame-by-frame
    ret, frame = cap.read()
    # x=cv2.GetMat(frame)
    # np_frame = np.asarray(x)
    # print(np_frame)
    print(frame.shape)
    # Our operations on the frame come here
    image=frame
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    #print(frame)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edged = cv2.Canny(blurred, 85, 85)
    lines = cv2.HoughLinesP(edged,1,np.pi/180,10,minLineLength,maxLineGap)
    if(lines !=None):
        for x in range(0, len(lines)):
            for x1,y1,x2,y2 in lines[x]:
                cv2.line(image,(x1,y1),(x2,y2),(0,255,0),2)
                theta=theta+math.atan2((y2-y1),(x2-x1))
   #print(theta)GPIO pins were connected to arduino for servo steering control
    threshold=6
    if(theta>threshold):
       #GPIO.output(7,True)
       #GPIO.output(8,False)
        p1.max()
        sleep(0.5)
        p1.mid()
        sleep(0.5)
        p1.max()
        sleep(0.5)
        p1.mid()
        print("left")
    if(theta<-threshold):
       #GPIO.output(8,True)
       #GPIO.output(7,False)
        q1.max()
        sleep(0.5)
        q1.mid()
        sleep(0.5)
        q1.max()
        sleep(0.5)
        q1.mid()
        print("right")
       
    if(abs(theta)<threshold):
      #GPIO.output(8,False)
      #GPIO.output(7,False)
       print ("straight")
    theta=0
    cv2.imshow("Frame",image)
    key = cv2.waitKey(1) & 0xFF
    np.trunc(frame)
    if key == ord("q"):
        break
