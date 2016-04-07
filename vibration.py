#!/usr/bin/python
"""
vibration.py
read temperature from GPIO#17 attached to SW-420

return true if vibration happens during 1 second interval
"""
import sys
import time
import RPi.GPIO as GPIO

def read_vibration():
    pin =17 

    boardRevision = GPIO.RPI_REVISION
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    vibrated = False
    start = time.time()

    while time.time() < start+1:
        if GPIO.input(pin):
            vibrated= True
            break

    return vibrated
