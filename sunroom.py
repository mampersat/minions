#!/usr/bin/python
import sys
import time
import requests
import json

from temperature import read_temperature
from lux import read_lux
from requests.auth import HTTPBasicAuth

my_id = 1
api = "http://192.168.1.116:8001/minions"

def send_to_ha(json_data):
    t = json_data['temp']
    h = json_data['humidity']
    l = json_data['lux']
    d = {
        "state": t,
        "attributes": {
            "unit_of_measurement": "F", "friendly_name": "Sunroom Temp"
            }
        }
    j = json.dumps(d)
    headers = {'x-ha-access': 'suzymatt', 'content-type': 'application/json'}

    r = requests.post("http://jarvis:8123/api/states/sensor.minion1_temp",
        data = j, headers=headers)
    print r.text

    d = { "state": l,
          "attributes": {
              "unit_of_measurement": "L", "friendly_name": "Sunroom Lux"
          }
    }
    j = json.dumps(d)
    r = requests.post("http://jarvis:8123/api/states/sensor.minion1_lux",
        data = j, headers=headers)
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
    # send_to_api(j)
    try:
      send_to_ha(p)
    except: 
      print("cant send to homeassistant")
    time.sleep(10)
