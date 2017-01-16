#!/usr/bin/python
"""
temperature.py
read temperature from GPIO#4 attached to DHT11
"""
import sys
import Adafruit_DHT
import json

def read_lux():
    pin = 4

    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)

    # Convert C->F
    temperature = temperature * 9.0/5.0 + 32

    if humidity is not None and temperature is not None:
        return humidity, temperature
    else:
        print 'Failed to get reading. Try again!'

def read_temperature_json(id):
    h,t = read_temperature()
    data = {}
    data['temp'] = t
    data['humidity'] = h
    data['id'] = id

    json_data = json.dumps(data)

    return json_data
