#!/usr/bin/python
"""
temperature.py
read temperature from GPIO#4 attached to DHT11
"""
import sys
import Adafruit_DHT

def read_temperature():
    sensor = 11
    pin = 4

    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)

    temperature = temperature * 9.0/5.0 + 32

    if humidity is not None and temperature is not None:
        print 'Temp={0:0.1f}*  Humidity={1:0.1f}%'.format(temperature, humidity)
        params = {'field1':temperature, 'field2':humidity, 'api_key':'HODM81D0JV0KYEIH'}
        return temperature, humidity
    else:
        print 'Failed to get reading. Try again!'
