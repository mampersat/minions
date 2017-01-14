#!/usr/bin/python
import sys
import time
import requests

from temperature import read_temperature

api = "http://192.168.1.114:8000/minions"
my_id = 1

def send_to_api(json):

    print json_data
    try:
        r=requests.post(api, data= json_data)
        print 'status code = {}'.format(r.status_code)
    except:
        print 'request error', sys.exc_info()[0]

while True:
    json = read_temperature_json()
    write_to_mysql(json)
    time.sleep(10)
