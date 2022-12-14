import sys
import RPi.GPIO as GPIO
import time
from time import sleep

signalBUZZERpin = 12
GPIO.setmode(GPIO.BCM)
GPIO.setup(signalBUZZERpin,GPIO.OUT,initial=GPIO.LOW)

def buzzFunction1():
    GPIO.output(signalBUZZERpin,1)
    time.sleep(0.5)
    GPIO.output(signalBUZZERpin,0)
    return
