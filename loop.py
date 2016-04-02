#!/usr/bin/python
import sys
import time
import requests

from Adafruit_IO import Client

from temperature import read_temperature

def write_to_thingspeak(t,h):
    
        # Here's an API key for ya. Thanks for reading my code! Submit some info
        params = {'field1':t, 'field2':h, 'api_key':'HODM81D0JV0KYEIH'}

        url = 'http://api.thingspeak.com/update'

        try:
            r = requests.post(url, data= params)
            print 'status code = {}'.format(r.status_code)
        except:
            print "request error"

def write_to_adafruit(t,h):
    aio = Client('3f755fc33a12977916bcbb1b518c8772ee16faaf')
    aio.send('minion1', t)
    
while True:
    humidity, temperature = read_temperature()

    if humidity is not None and temperature is not None:
        print 'Temp={0:0.1f}*  Humidity={1:0.1f}%'.format(temperature, humidity)

    write_to_thingspeak(temperature, humidity)
    write_to_adafruit(temperature, humidity)

    time.sleep(10)
