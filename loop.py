#!/usr/bin/python
import sys
import time
import requests
import json

from Adafruit_IO import Client
from temperature import read_temperature

api = "http://192.168.1.114:8000/minions"
my_id = 1

def write_to_mysql(t,h):
    data = {}
    data['temp'] = t
    data['id'] = my_id

    json_data = json.dumps(data)

    print json_data
    try:
        r=requests.post(api, data= json_data)
        print 'status code = {}'.format(r.status_code)
    except:
        print 'request error', sys.exc_info()[0]

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
    try:
        aio = Client('3f755fc33a12977916bcbb1b518c8772ee16faaf')
        aio.send('minion1', t)
    except:
        print "request error"

    
while True:
    humidity, temperature = read_temperature()

    if humidity is not None and temperature is not None:
        print 'Temp={0:0.1f}*  Humidity={1:0.1f}%'.format(temperature, humidity)

    # write_to_thingspeak(temperature, humidity)
    # write_to_adafruit(temperature, humidity)
    write_to_mysql(temperature, humidity)


    time.sleep(10)
