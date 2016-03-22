#!/usr/bin/python
import sys
import time
import requests

from temperature import read_temperature

while True:
    humidity, temperature = read_temperature()

    if humidity is not None and temperature is not None:
        print 'Temp={0:0.1f}*  Humidity={1:0.1f}%'.format(temperature, humidity)
        # Here's an API key for ya. Thanks for reading my code! Submit some info
        params = {'field1':temperature, 'field2':humidity, 'api_key':'HODM81D0JV0KYEIH'}

        url = 'http://api.thingspeak.com/update'
        r = requests.post(url, data= params)
        print 'status code = {}'.format(r.status_code)
    else:
        print 'Failed to get reading. Try again!'

    time.sleep(10)
