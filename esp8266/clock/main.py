""" LED Strip Control

Control led lights based on MQTT messages
"""
import machine
import math
import neopixel
import network
import ntptime
import time
import uos
from umqtt.simple import MQTTClient

pin = 4
lights = 8
np = neopixel.NeoPixel(machine.Pin(pin), lights)


def allOff():
    """ Turn all the lights off
    """
    print("allOff")
    for i in range(0, np.n):
        np[i] = (0, 0, 0)
    np.write()


def knight_rider(loop=100, delay=50):
    """ Show Knight Rider animation
    loop = number of loops
    delay = sleep time between steps
    based on sin function
    """
    periods = 16

    # syncrhonize the two cos waves
    # this math is based on measurements vs. understanding what's going on
    np_div = np.n / 3.3

    t = 0
    for i in range(0, loop):
        t += 1
        for p in range(0, np.n):

            # this controls speed - higher is faster
            f = t * 3.2

            v1 = math.cos(f / periods + p/np_div) - 0.7
            v1 = max(0, v1)

            v2 = math.cos(-f / periods + p/np_div) - 0.7
            v2 = max(0, v2)

            b = int(v1 * 50) + int(v2 * 50)

            np[p] = (b, 0, 0)

        np.write()
        time.sleep_ms(delay)


def connect_and_sync():
    """ Attempt wifi connection and ntp synchronization
    """

    w = network.WLAN(network.STA_IF)
    while not w.isconnected():
        # s.connect('ShArVa')
        print("Network not connected - sleeping")
        knight_rider()

    print("Netowrk connected")
    knight_rider(200, 10)

    ntp_sync = False
    while not ntp_sync:
        try:
            print("NTP time sync")
            ntptime.settime()
        except:
            print("NTP fail")
            knight_rider(100, 5)
        else:
            print("NTP synced")
            ntp_sync = True

    knight_rider(200,0)

def hour_glass():
    """ Display system clock binary
    first bit = 14.0625s
    """

    color_array = [
        (13, 13, 13),   # 9-10am-White
        (13, 13, 0),   # 10-11am-Yellow
        (0, 13, 0),   # 11-12pm-Green
        (13, 0, 0),   # 12-1pm-Red
        (13, 13, 13),   # 1-2pm-White
        (13, 13, 0),   # 2-3pm-Yellow
        (0, 13, 0),   # 3-4pm-Green
        (13, 0, 0),   # 5pm-6pm-Red
        (13, 0, 0),   # 8-9am-Red

    ]

    # ntptime.settime()
    # machine.RTC().datetime((2018, 5, 13, 0, 10, 59, 40, 0)) #  Test top of the hour
    connect_and_sync()

    nr = False

    while True:

        t = machine.RTC().datetime()
        h = t[4]
        m = t[5]
        s = t[6]
        c = m * 60 + s
        b = int(c / 14.0625)

        # top of the hour - show night rider
        if (m == 0):
            if not nr:
                connect_and_sync()
                nr = True
        else:
            nr = False

        for p in range(0, np.n):
            if (b & pow(2, p)):
                np[p] = color_array[h % 9]
            else:
                np[p] = (0, 0, 0)
        np.write()

        print("h= {}, m= {}, s= {}, b= {}".format(h, m, s, b))
        time.sleep_ms(500)


""" Main control logic
"""

allOff()

hour_glass()

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
