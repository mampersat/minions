""" LED Strip Control

Control led lights based on MQTT messages
"""
import machine
import math
import neopixel
import network
import time
import uos

from umqtt.simple import MQTTClient

pin = 4
topic = 'leds'
broker = 'jarvis'
client = MQTTClient('leds', broker)
lights = 128
np = neopixel.NeoPixel(machine.Pin(pin), lights)


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

def night_rider_1():
    """ Night rider red wave animation
    based on mod and abs functions
    """
    tf = 14
    for t in range(0, 10000):
        for p in range(0, np.n):
            pm = p % 8
            v = (tf/2) - abs(pm - abs((t % tf)-(tf / 2)))
            v = int(v)
            if v == 7:
                np[p] = (10, 0, 0)
            elif v == 6:
                np[p] = (1, 0, 0)
            else:
                np[p] = (0, 0, 0)

        np.write()
        time.sleep_ms(100)


def night_rider_2():
    """ Night rider red wave animation
    based on sin function
    """

    periods = 16

    # syncrhonize the two cos waves
    # this math is based on measurements vs. understanding what's going on
    np_div = np.n / 3.3

    t = 0
    while True:
        t += 1
        for p in range(0, np.n):

            # this controls speed - higher is faster
            f = t * 3.2

            v1 = math.cos(f / periods + p/np_div) - 0.7
            v1 = max(0, v1)

            v2 = math.cos(-f / periods + p/np_div) - 0.7
            v2 = max(0, v2)

            r = int(v1 * 50) + int(v2 * 50)

            np[p] = (r, 0, 0)

        np.write()
        # time.sleep_ms(10)


def bin_walk():
    t = 0
    while True:
        t = t + 1
        for p in range(0, np.n):
            if (t & pow(2, p)):
                np[p] = (5, 5, 5)
            else:
                np[p] = (0, 0, 0)
        np.write()

        time.sleep(0)

def bin_walk_2():
    """ Faster binary ticker
    Logic = Find a light to turn on - turn off all before
    """
    b = 0
    while True:
        # find the first OFF bit
        t = 0
        while (b & pow(2, t)):
            t += 1

        np[t] = (5, 5, 5)
        for i in range(0, t):
            np[i] = (0, 0, 0)
        np.write()

        b += 1


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
# startUpAllOn()
# night_rider_2()
# bin_walk()
bin_walk_2()

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
