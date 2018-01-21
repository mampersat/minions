""" Model House Light Control

Control led lights in model house based on MQTT messages
"""
import machine
import network
import time
from umqtt.simple import MQTTClient

topic = 'model'
broker = '192.168.1.117' #'jarvis'
client= MQTTClient('model', broker)

led = machine.Pin(16, machine.Pin.OUT)


def gotMessage(topic, msg):
    print(msg)
    if msg == b'on':
        led.on()
        print("Turn On")

    if msg == b'off':
        led.off()
        print("Turn Off")


client.set_callback(gotMessage)

s = network.WLAN(network.STA_IF)
while not s.isconnected():
    # s.connect('ShArVa')
    print("Network not connected - sleeping")
    time.sleep(1)

print(s.ifconfig())

connected = False
while not connected:
    try:
        print("Connecting")
        client.connect()
    except:
        print("Connection Fail")
        time.sleep(1)
    else:
        connected = True

print("Connected")

client.subscribe(b"model/light")

while True:
    client.wait_msg()

    print("Waiting")
    time.sleep(1)
