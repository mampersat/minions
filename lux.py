#!/usr/bin/python
"""
temperature.py
read temperature from GPIO#4 attached to DHT11
"""
import sys
import Adafruit_DHT
import json
import RPi.GPIO as GPIO
import time
import os

def read_lux(p):
    RCpin = 18
    GPIO.setmode(GPIO.BCM)

    reading = 0
    GPIO.setup(RCpin, GPIO.OUT)
    GPIO.output(RCpin, GPIO.LOW)
    #Charge the capictor
    time.sleep(0.1)

    GPIO.setup(RCpin, GPIO.IN)
    # see how long it takes to discharge
    while (GPIO.input(RCpin) == GPIO.LOW):
            reading += 1

    p['lux'] = reading
    
