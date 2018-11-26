""" Motor Cycle Weather Status

Control led lights based on Dark Sky weather predictions
"""
import json
import machine
import math
import neopixel
import network
import ntptime
import urequests
import time

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

    attempts = 4  # How many times to attempt network connection
    while not w.isconnected():
        # s.connect('ShArVa')
        print("Network not connected - sleeping")
        knight_rider()

        attempts -= 1
        if not attempts:
            return()

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

    knight_rider(200, 0)


def motorcycleability():
    """ Display forecast information with regard to motorcycle riding
    Get rain etc. for next time 8-10am block or next 4-6pm block
    """

    # ntptime.settime()
    # machine.RTC().datetime((2018, 5, 13, 0, 10, 59, 40, 0)) #  Test top of the hour
    connect_and_sync()
    url = "https://api.darksky.net/forecast/73aaae75acf106e62591ff108c364d81/37.8267,-122.4233"
    headers = {'Accept-Encoding':'gzip'}
    r = urequests.get(url, headers = headers)
    print(r.content)
    j = json.loads(r.content)
    rain = j['hourly']['data'][0]['precipProbability']
    i = 0

    for h in j['hourly']['data']:
        t = h.get('time')
        p = h.get('precipProbability')
        np[i] = (255 * p, 0 ,0 )
    np.write()



    nr = False
    lb = -1

    while True:

        t = machine.RTC().datetime()
        h = t[4]

        print("time after time")
        time.sleep(100)


""" Main control logic
"""

allOff()

motorcycleability()
