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
lights = 8
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
            f = t * 1.5

            v1 = math.cos(f / periods + p/np_div) - 0.7
            v1 = max(0, v1)

            v2 = math.cos(-f / periods + p/np_div) - 0.7
            v2 = max(0, v2)

            r = int(v1 * 50) + int(v2 * 50)

            np[p] = (r, 0, 0)

        np.write()
        # time.sleep_ms(10)


def bin_walk():
    """ Display incrementing binary digit
    """
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
    """ Display incrementing binary digit
    Only make neopixel changes that are necessary - faster
    16 lights = 00:03:17
    39 lights ~ 100 years
    """
    b = 0
    while True:
        # find the first OFF bit
        # probably a better way to do this with log() etc
        t = 0
        while (b & pow(2, t)):
            t += 1

        # is this the last bit on the strip
        if (t == np.n):
            b = 0
            time.sleep(1)
        else:
            np[t] = (5, 5, 5)
            # np[t] = (uos.urandom(1)[0], uos.urandom(1)[0], uos.urandom(1)[0])

        for i in range(0, t):
            np[i] = (0, 0, 0)
        np.write()

        b += 1

        # time.sleep_ms(168750) # 8 bits = 6 hours
        time.sleep_ms(14063)  # 8 bits = 30min


def bin_walk_3():
    """ Display time in 8 bits

    """
    b = 0
    c = 0
    color_array = [
        (13, 0, 0),   # 8-9am-Red
        (13, 13, 13),   # 9-10am-White
        (13, 13, 0),   # 10-11am-Yellow
        (0, 13, 0),   # 11-12pm-Green
        (13, 0, 0),   # 12-1pm-Red
        (13, 13, 13),   # 1-2pm-White
        (13, 13, 0),   # 2-3pm-Yellow
        (0, 13, 0),   # 3-4pm-Green
        (13, 0, 0),   # 5pm-6pm-Red
    ]

    while True:
        # find the first OFF bit
        # probably a better way to do this with log() etc
        t = 0
        while (b & pow(2, t)):
            t += 1

            # is this the 8th bit - i.e. an hour has passed
            if (t == 8):
                c += 1
                c =c % 9

        # is this the last bit on the strip
        if (t == np.n):
            b = 0
            time.sleep(1)
        else:
            # np[t] = (5, 5, 5)
            # np[t] = (uos.urandom(1)[0], uos.urandom(1)[0], uos.urandom(1)[0])
            np[t] = color_array[c]

        for i in range(0, t):
            np[i] = (0, 0, 0)
        np.write()

        b += 1

        time.sleep_ms(14063)  # ~ 15s8 bits = 30min
        #time.sleep_ms(100)

def hour_glass():
    """ Display system clock minutes in binary
    first bit = 14.0625s
    """
    m = machine.RTC().datetime()[5]  # current minute
    b = int(m / 14.0625)

    while True:
        for p in range(0, np.n):
            if (b & pow(2, p)):
                np[p] = (5, 5, 5)
            else:
                np[p] = (0, 0, 0)
        np.write()

        print("m= {}, b= {}".format(m,b))
        time.sleep(500)

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
night_rider_2()
# bin_walk()
# bin_walk_3()
# hour_glass()

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
