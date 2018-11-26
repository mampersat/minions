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

last_message = {}


def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("/strip/health/#")


def display():
    os.system('cls' if os.name == 'nt' else 'clear')
    now = datetime.datetime.now()

    for m in last_message:
        # print m
        client = m.split('/')[3]
        # print client
        name = fleet[client]
        p = last_message[m][0]
        t = last_message[m][1]
        d = now - t

        print("{}\t{}\t{}".format(name, p, d.total_seconds()))


def on_message(client, userdata, msg):
    global last_message
    print(msg.topic+" "+str(msg.payload))
    last_message[msg.topic] = (msg.payload, datetime.datetime.now())

    display()


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("192.168.1.132")

while True:
    client.loop()