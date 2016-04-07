#!/usr/bin/python
import sys
import time
import requests
import RPi.GPIO as GPIO

from Adafruit_IO import Client

from temperature import read_temperature

vibration_time = time.time()
motion_time = time.time()

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
        aio.send('minion2', t)
    except:
        print("request error")

def write_no_motion_to_adafruit():
    global motion_time
    print("no motion")
    motion_time = time.time()
    try:
        aio = Client('3f755fc33a12977916bcbb1b518c8772ee16faaf')
        aio.send('minion2-motion', 0)
    except:
        print("request error")

def write_motion_to_adafruit(chan):
    global motion_time
    print("motion")
    motion_time = time.time()
    try:
        aio = Client('3f755fc33a12977916bcbb1b518c8772ee16faaf')
        aio.send('minion2-motion', 1)
    except:
        print("request error")

def write_vibration_to_adafruit(chan):
    global vibration_time
    print("vibration")
    vibration_time = time.time()
    try:
        aio = Client('3f755fc33a12977916bcbb1b518c8772ee16faaf')
        aio.send('minion2-vibration', 1)
    except:
        print("request error")


def write_still_to_adafruit():
    print("still")
    vibration_time = time.time()
    try:
        aio = Client('3f755fc33a12977916bcbb1b518c8772ee16faaf')
        aio.send('minion2-vibration', 0)
    except:
        print("request error")

GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(9, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(17, GPIO.RISING, callback=write_vibration_to_adafruit, bouncetime=2000)
GPIO.add_event_detect(9, GPIO.RISING, callback=write_motion_to_adafruit, bouncetime=2000)
    
while True:
    humidity, temperature = read_temperature()

    if humidity is not None and temperature is not None:
        print 'Temp={0:0.1f}*  Humidity={1:0.1f}%'.format(temperature, humidity)

    write_to_thingspeak(temperature, humidity)
    write_to_adafruit(temperature, humidity)

    print("Sleeping 10s")
    time.sleep(10)

    #write "still" if vibration time is>20 seconds
    if (time.time() - vibration_time) >20:
        write_still_to_adafruit()

    #write "no motion" if motion time is > 20seconds
    if (time.time() - motion_time) > 20:
        write_no_motion_to_adafruit()

