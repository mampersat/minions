"""
main.py
read temperature from ADC pin and publish to mqtt
"""

import machine
import math
import network
import time
import ubinascii
import uos
from umqtt.simple import MQTTClient

motd = "2018-11-24 bbq temperature"

broker = 'jarvis'
client_id = 'esp8266_'+str(ubinascii.hexlify(machine.unique_id()), 'utf-8')
print("client_id = "+client_id)
topic = 'strip/' + client_id
client = MQTTClient(topic, broker)
print("listening to ", broker, " for ", topic)

adc = machine.ADC(0)

def time_check():
    publish("time check")
    client.check_msg()
    try:
        ntptime.settime()
    except:
        print(".")


def frangable_publish(topic, payload):
    try:
        client.publish(topic, payload)
        print("Wrote", payload, " to ", topic)
    except:
        print("failed to log, sleeping 1")
        time.sleep(1)
        try:
            client.connect()
        except:
            print("failed to connect")


def publish(message):
    frangable_publish("/bbq/" + client_id, message)


s = network.WLAN(network.STA_IF)
while not s.isconnected():
    publish("Network not connected - sleeping")
    time.sleep(1)

print(s.ifconfig())

connected = False
while not connected:
    try:
        client.connect()
    except:
        print(".")
        time.sleep(1)
    else:
        connected = True
publish("alive " + motd + ' ' + s.ifconfig()[0])


while True:
    v = adc.read()
    v_i = int(v)

    # this 6.2 isn't a constant
    # some calibration shows it is accurate around 165 freedom degrees
    # which is our target for cooking a turkey
    #t = v_i / 6.2

    publish(str(v_i))
    time.sleep_ms(250)
