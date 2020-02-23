import machine
import math
import neopixel
import network
import os
import time
import ubinascii
import uos  # random numbers
import utime
import urequests

pin = 14
lights = 50
level = 10

np = neopixel.NeoPixel(machine.Pin(pin), lights)

np[0] = (0,10,0)
np.write()

def random(i=1):
    if (i != 1):
        return int(uos.urandom(1)[0]/256 * i)
    else:
        return uos.urandom(1)[0]/256

while True:
    t = int( utime.ticks_ms() / 1000 )
    for i in range(0,50):

        i_prime = i % 10

        v = int( t / pow (3, i_prime)) % 3

        r = (v == 0) * 10
        g = (v == 1) * 10
        b = (v == 2) * 10

        print(r, g, b)

        np[i] = ( r, g, b)

    np.write()