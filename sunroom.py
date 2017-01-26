#!/usr/bin/python
import sys
import time
import requests
import json

from temperature import read_temperature
from lux import read_lux

my_id = 1
api = "http://192.168.1.114:8000/minions"

def send_to_ha(json_data):
    t = json_data['temp']
    h = json_data['humidity']
    d = {
        "state": t,
        "attributes": {
            "unit_of_measurement": "F", "friendly_name": "Minion 1 Temp"
            }
        }
    j = json.dumps(d)
    r = requests.post("http://192.168.1.114:8123/api/states/sensor.minion1_temp",
        data = j)
    print r.text

def send_to_api(json_data):

    print json_data
    try:
        r=requests.post(api, data= json_data)
        print 'status code = {}'.format(r.status_code)
    except:
        print 'request error', sys.exc_info()[0]

while True:
    p = {"id":my_id}
    read_temperature(p)
    read_lux(p)
    j = json.dumps(p)
    send_to_api(j)
    send_to_ha(p)
    time.sleep(10)
