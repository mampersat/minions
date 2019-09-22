#!/usr/bin/env python

""" monitor.py
listen on mqtt and represent messages from light strips
Highlight heartbeats
"""

import datetime
import os
import paho.mqtt.client as mqtt

# Map to current deployments
fleet = {}
fleet['esp8266_8f141200'] = "Master East"
fleet['esp8266_8b0e1200'] = "Master West"
fleet['esp8266_51333700'] = "desk window"
fleet['esp8266_5133d500'] = 5
fleet['esp8266_609a1100'] = "breadboard"
fleet['esp8266_7f35d500'] = "tester"
fleet['esp8266_c1584a00'] = "3x5"
fleet['esp8266_22584a00'] = "Test Block"
fleet['esp8266_a84b4a00'] = "Master East"



last_message = {}


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def humanize(second_diff):
    day_diff = int(second_diff/60/60/24)

    if day_diff < 0:
        return ''

    if day_diff == 0:
        if second_diff < 10:
            return "just now"
        if second_diff < 60:
            return str(int(second_diff)) + " seconds ago"
        if second_diff < 120:
            return "a minute ago"
        if second_diff < 3600:
            return str(int(second_diff / 60)) + " minutes ago"
        if second_diff < 7200:
            return "an hour ago"
        if second_diff < 86400:
            return str(int(second_diff / 3600)) + " hours ago"
    if day_diff == 1:
        return "Yesterday"
    if day_diff < 7:
        return str(day_diff) + " days ago"
    if day_diff < 31:
        return str(day_diff / 7) + " weeks ago"
    if day_diff < 365:
        return str(day_diff / 30) + " months ago"
    return str(day_diff / 365) + " years ago"


def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("/strip/health/#")


def display():
    os.system('cls' if os.name == 'nt' else 'clear')
    now = datetime.datetime.now()
    
    print("Time: {}".format(now))

    for m in last_message:
        # print m
        client = m.split('/')[3]
        # print client
        if client in fleet:
            name = fleet[client]
        else:
            name = client
        p = last_message[m][0]
        t = last_message[m][1]
        d = (now - t)
        s = d.total_seconds()
        color = ''
        if (s < 300):
            color = bcolors.OKGREEN
        elif (s < 3000):
            color = bcolors.WARNING
        else:
            color = bcolors.FAIL

        human = humanize(s)

        # print(color + "{}\t{}\t{}".format(name, p, d.total_seconds()) + bcolors.ENDC)
        print(color + "{}\t{}\t{}".format(name, p, human) + bcolors.ENDC)


def on_message(client, userdata, msg):
    global last_message
    # print(msg.topic+" "+str(msg.payload))
    last_message[msg.topic] = (msg.payload, datetime.datetime.now())


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("jarvis")

while True:
    client.loop()
    display()
