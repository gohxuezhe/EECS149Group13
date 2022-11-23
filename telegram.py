from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2

import telepot
import os
from picamera import PiCamera
import RPi.GPIO as GPIO
import time
from time import sleep
import datetime
from telepot.loop import MessageLoop
from subprocess import call 


# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 25

bot = telepot.Bot('5721555744:AAGpA-DJt1kBkdO10KcZVX3KMvua2U2I8Nk')


def sendNotification(): 
    global chat_id
    captureCheck=False
    time.sleep(0.1) # allow the camera to warmup
    
    while True:
        rawCapture1 = PiRGBArray(camera, size=(640, 480)) # grab the raw NumPy array representing the image
        camera.capture(rawCapture1, format="bgr")
        frame1 = rawCapture1.array
        gray1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
        gray1 = cv2.GaussianBlur(gray1, (21, 21), 0)

        rawCapture2 = PiRGBArray(camera, size=(640, 480))
        camera.capture(rawCapture2, format="bgr")
        frame2 = rawCapture2.array
        gray2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
        gray2 = cv2.GaussianBlur(gray2, (21, 21), 0)

        deltaframe=cv2.absdiff(gray1,gray2)
        threshold = cv2.threshold(deltaframe, 25, 255, cv2.THRESH_BINARY)[1]
        threshold = cv2.dilate(threshold,None)
        countour,heirarchy = cv2.findContours(threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        print("hi")
        for i in countour:
            if cv2.contourArea(i) < 7000:
                continue

            (x, y, w, h) = cv2.boundingRect(i)
            cv2.rectangle(frame2, (x, y), (x + w, y + h), (255, 0, 0), 2)
            captureCheck=True;
        

        cv2.imshow('window1',frame2)
        if captureCheck:
            cv2.imwrite('frame.jpg',frame2)
            bot.sendPhoto(chat_id, photo = open('frame.jpg', 'rb'))
            bot.sendMessage(chat_id, 'The motion sensor is triggered!')
            captureCheck=False;

        key = cv2.waitKey(1) & 0xFF

        # clear the stream in preparation for the next frame
        rawCapture1.truncate(0)
        rawCapture2.truncate(0)

        # if the `q` key was pressed, break from the loop
        if key == ord("q"):
            break

def main(msg):
    global telegramText 
    telegramText = msg['text']
    global chat_id
    chat_id = msg['chat']['id']

    print('Message received from ' + str(chat_id))

    if telegramText != '/start':
        bot.sendMessage(chat_id, 'wrong start code')
        return

    bot.sendMessage(chat_id, 'Security camera is activated.')
    print("Motion detected")
    sendNotification()
    time.sleep(10)
    return 

bot.message_loop(main)
while 1:
    time.sleep(10)