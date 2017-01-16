#!/usr/bin/python
"""
temperature.py
read temperature from GPIO#4 attached to DHT11
"""
import sys
import Adafruit_DHT
import json

def read_temperature(p):
    sensor = 11
    pin = 4

    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)

    # Convert C->F
    temperature = temperature * 9.0/5.0 + 32

    if humidity is None or temperature is None:
        print 'Failed to get reading. Try again!'
        return

    p['temp'] = temperature
    p['humidity'] = humidity
