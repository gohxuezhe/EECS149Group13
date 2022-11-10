import telepot
import os
from picamera import PiCamera
import RPi.GPIO as GPIO
import time
from time import sleep
import datetime
from telepot.loop import MessageLoop
from subprocess import call 

camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 25

bot = telepot.Bot('INSERT KEY')


def sendNotification(): 
  global chat_id
  filename = "./video_" + (time.strftime("%y%b%d_%H%M%S"))
  camera.start_recording(filename + ".h264")
  sleep(5)
  camera.stop_recording()
  command = "MP4Box -add " + filename + '.h264' + " " + filename + '.mp4'
  print(command)
  call([command], shell=True)
  bot.sendVideo(chat_id, video = open(filename + '.mp4', 'rb'))
  bot.sendMessage(chat_id, 'The motion sensor is triggered!') 
  os.remove(filename + '.mp4');
  os.remove(filename + '.h264');

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

bot.message_loop(main)
while 1:
 time.sleep(10)