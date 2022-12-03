from picamera.array import PiRGBArray
from picamera import PiCamera
import cv2

import telegram
from telegram.ext.updater import Updater
from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.commandhandler import CommandHandler
from telegram.ext.messagehandler import MessageHandler
from telegram.ext.filters import Filters

import os
import RPi.GPIO as GPIO
import time
from time import sleep
import datetime

#from image import *
from game import *

# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 25

bot = telegram.Bot('5721555744:AAGpA-DJt1kBkdO10KcZVX3KMvua2U2I8Nk')
try:
    chat_id = bot.get_updates()[-1].message.chat_id
except IndexError:
    chat_id = 0

def startSecurity(): 
    global chat_id
    captureCheck=False
    time.sleep(0.1) # allow the camera to warmup
    
    while True:
        captureCheck=False
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
        i=0
        for j in countour:
            if cv2.contourArea(j) < 7000:
                continue

            (x, y, w, h) = cv2.boundingRect(j)
            cv2.rectangle(frame2, (x, y), (x + w, y + h), (255, 0, 0), 2)
            captureCheck=True;
        
        cv2.imshow('window1',frame2)
        if captureCheck:
            cv2.imwrite('frame.jpg',frame2)
            model = load_model("game-model.h5")
            for i in range(10):
                print("i is: ",i)
                test=gameFunction(camera,model)
                print("gameFunction is: ",test)
                if test==True:
                    print("gameFunction is verified")
                    time.sleep(3)
                    break
                elif test==False:
                    print("gameFunction not verified")
                if i==9:
                    bot.sendPhoto(chat_id, photo = open('frame.jpg', 'rb'))
                    bot.sendMessage(chat_id, 'The motion sensor is triggered!')
                    captureCheck=False;
                time.sleep(1)

        key = cv2.waitKey(1) & 0xFF

        # clear the stream in preparation for the next frame
        rawCapture1.truncate(0)
        rawCapture2.truncate(0)

        # if the `q` key was pressed, break from the loop
        if key == ord("q"):
            break

updater = Updater("5721555744:AAGpA-DJt1kBkdO10KcZVX3KMvua2U2I8Nk",use_context=True)


def start(update: Update, context: CallbackContext):
    update.message.reply_text("start selected")
    startSecurity()

def help(update: Update, context: CallbackContext):
    update.message.reply_text("help selected")
    update.message.reply_text(
    '''
    -input '/start' to start security
    
-input '/train' to start data collection and training
    '''
    )

def train(update: Update, context: CallbackContext):
    update.message.reply_text("train selected")

def unknown(update: Update, context: CallbackContext):
    update.message.reply_text("Sorry '%s' is not a valid command, input '/help' to find out the commands" % update.message.text)

def unknown_text(update: Update, context: CallbackContext):
    update.message.reply_text("Sorry I can't recognize you , you said '%s', input '/help' to find out the commands" % update.message.text)

updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('train', train))
updater.dispatcher.add_handler(CommandHandler('help', help))
updater.dispatcher.add_handler(MessageHandler(Filters.text, unknown))
updater.dispatcher.add_handler(MessageHandler(Filters.command, unknown)) # Filters out unknown commands

# Filters out unknown messages.
updater.dispatcher.add_handler(MessageHandler(Filters.text, unknown_text))

updater.start_polling()