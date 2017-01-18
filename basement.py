#!/usr/bin/python
import sys
import time
import requests
import json
import socket
import fcntl
import struct

from temperature import read_temperature
from lux import read_lux
from led import flash_msg

api = "http://192.168.1.114:8000/minions"
my_id = 2

def send_to_api(json_data):

    print json_data
    try:
        r=requests.post(api, data= json_data)
        print 'status code = {}'.format(r.status_code)
    except:
        print 'request error', sys.exc_info()[0]
""" 
sad - fix for on startup not being connected
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
ip = socket.inet_ntoa(fcntl.ioctl(
    s.fileno(),
    0x8915,  # SIOCGIFADDR
    struct.pack('256s', "wlan0")
)[20:24])
print ip
l4 = ip.split('.')[3]
print l4
"""
l4='000'

while True:
    p = {"id":my_id}
    read_temperature(p)
    # read_lux(p)
    j = json.dumps(p)
    send_to_api(j)
    flash_msg(l4)
