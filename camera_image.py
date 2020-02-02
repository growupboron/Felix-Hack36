

import cv2
import time
import os
import sys
import signal 

camera_port = 0
 

ramp_frames = 5
display = "Display Window"
file = "scene.png"


def exit_gracefully(signum,frame):
    signal.signal(signal.SIGINT, original_sigint)
    sys.exit(1)
 

def get_image(camera):
    retval, im = camera.read()
    return im

def take_save_image(camera): 
    
    camera_capture = get_image(camera)
    cv2.imwrite(file, camera_capture)
    #cv2.imshow(display, camera_capture)
 

def run_main():
    
    camera = cv2.VideoCapture(camera_port)
   
      
    for i in xrange(ramp_frames):
        temp = get_image(camera)

   
    i=1
    while(i!=0):
        try:
            time.sleep(1)
            take_save_image(camera)
        except Exception, e:
            print "Exception occured \n"
            print e
            pass
        i=0
        
        

if __name__ == '__main__':
    original_sigint = signal.getsignal(signal.SIGINT)
    signal.signal(signal.SIGINT,exit_gracefully)
    run_main()
os.system("python ms_visionapi.py")
