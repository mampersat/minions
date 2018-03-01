""" LED Strip Control

Control led lights based on MQTT messages
"""
import machine
import neopixel
import network
import time
import uos

from umqtt.simple import MQTTClient

topic = 'leds'
broker = '192.168.1.117'  # 'jarvis'
client = MQTTClient('leds', broker)
lights = 53
np = neopixel.NeoPixel(machine.Pin(2), lights)


def allOff():
    """ Turn all the lights off
    """
    print("allOff")
    for i in range(0, np.n):
        np[i] = (0, 0, 0)
    np.write()


def startUpAllOn():
    """ Turn all the lights on starting from the edges
    """
    print("startUpAllOn")
    for i in range(0, np.n / 2):
        np[i] = (10, 10, 10)
        np[(np.n - i) - 1] = (10, 10, 10)
        time.sleep_ms(10)
        np.write()

def party():
    """ Show a lot of colors and animation
    """
    print("Party")
    for i in range(0, np.n):
        np[i] = (uos.urandom(1)[0], uos.urandom(1)[0], uos.urandom(1)[0])

    np.write()

def gotMessage(topic, msg):
    print(topic)
    print(msg)

    # Address single light via topc - disabled
    # light = int(topic.decode("utf-8").split('/')[-1])

    if msg == b'on':
        startUpAllOn()

    if msg == b'off':
        allOff()

    if msg == b'party':
        party()
        print("Party")


""" Main control logic

Initialize neopixels
Connect to network
Register Callbacks
start main loop
"""

allOff()
startUpAllOn()

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

client.subscribe(b"strip/anet")

while True:
    client.wait_msg()
