import tkinter as tk
from picamera import PiCamera
from time import sleep
from gpiozero import Button, LED
import datetime
import pyrebase
import datetime
import cv2
import numpy as np
import matplotlib 
import matplotlib.pyplot as plt
import imutils

config = {
  "apiKey": "AIzaSyB7OYWCl0E--yBs0v0zhCYpQhGccXR4PPw",
  "authDomain": "pi-cloud-e4ce4.firebaseapp.com",
  "databaseURL": "https://pi-cloud-e4ce4-default-rtdb.asia-southeast1.firebasedatabase.app",
  "projectId": "pi-cloud-e4ce4",
  "storageBucket": "pi-cloud-e4ce4.appspot.com",
  "messagingSenderId": "693267834031",
  "appId": "1:693267834031:web:5342f37926600dfaffe05a",
  "measurementId": "G-SERYYK1E3F"        
}

firebase = pyrebase.initialize_app(config)
storage = firebase.storage()

led = LED(18)
camera = PiCamera()

root = tk.Tk()
root.geometry("400x200")

def my_function():
    print("Button pressed!")
    camera.exposure_mode = 'antishake'
    filename = datetime.datetime.now().strftime("%Y-%m-%d-%H:%M:%S")
    filepath = "/home/abhishek/Desktop/PiVideos/" + filename + ".h264"

    camera.start_recording(filepath)
    led.on()
    sleep(5)
    camera.stop_recording()
    led.off()

    path_on_cloud = "videos/" + filename + ".h264"
    path_local = filepath
    storage.child(path_on_cloud).put(path_local)
    storage.child(path_on_cloud).download("/home/abhishek/Desktop/PiVideos/fromCloud/" + filename + "_dwld.h264")

    cap = cv2.VideoCapture(filepath)
    maxIntensity = 0.00
    while(cap.isOpened()):
        ret, frame = cap.read()
        if ret == True:
            frame = cv2.resize(frame,(400,200))
            cv2.imshow('original',frame)
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            light_blue = np.array([100,50,50])
            dark_blue = np.array([130,255,255])
            mask = cv2.inRange(hsv, light_blue, dark_blue)
            mask2 = cv2.resize(mask, (400,200))
            meanValue = np.mean(mask)
            print('mean blue color = ', meanValue)
            if(maxIntensity < meanValue):
                maxIntensity = meanValue
            #result = cv2.bitwise_and(frame,frame,mask=mask)
            cv2.imshow('mask', mask2)
            cv2.waitKey(50)
        if ret == False: 
            break
    print('maximum intensity light: ', maxIntensity)
    cap.release()
    cv2.destroyAllWindows()

button = tk.Button(root, text = "Calculate Intensity", command = my_function)
button.pack()
root.mainloop()

