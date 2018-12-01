import datetime
import os
import paho.mqtt.client as mqtt

fleet = {}
fleet['esp8266_8f141200'] = "master east       "
fleet['esp8266_8b0e1200'] = "master west       "
fleet['esp8266_51333700'] = "Nick west         "
fleet['esp8266_5133d500'] = "Nick east         "
fleet['esp8266_609a1100'] = "office window east"
fleet['esp8266_7f35d500'] = "test 4x8          "

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

client = mqtt.Client()
client.on_connect = on_connect

client.connect("192.168.1.132")
