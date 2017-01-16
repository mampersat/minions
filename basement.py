#!/usr/bin/python
import sys
import time
import requests
import json

from temperature import read_temperature
from lux import read_lux

api = "http://192.168.1.114:8000/minions"
my_id = 2

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
    time.sleep(10)
