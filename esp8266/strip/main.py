import machine
import math
import neopixel
import network
import time
import ubinascii
import uos # random numbers
import utime
# import config

pin = 14
topic = 'leds'
broker = 'jarvis'
lights = 150
level = 100
mode = "ho"

np = neopixel.NeoPixel(machine.Pin(pin), lights)

# fall
pallet = [
    (10, 0, 0),      # red
    (0, 10, 0),      # green
    (10, 10, 0),    # yellow
    (30, 5, 0),    # orange
]

strip_tester = [
    [2, 1, 0, 21, 20, 19, 17],
    [6, 8, 9, 10, 11, 12, 13]
]

strip = [[],[]]
for i in range(49, 93):
    strip[0].append(i)

for i in range(22, 2, -1):
    strip[1].append(i)

for i in range(143,  120, -1):
    strip[1].append(i)
    
def random(i):
    if i:
        return int(uos.urandom(1)[0]/256 * i)
    else:
        return uos.urandom(1)[0]/256

def keep_running():
    if utime.ticks_ms() < 50000: # about 30s
        return True
    else:
        print("resetting")
        machine.reset()

def allOff():
    for i in range(0, np.n):
        np[i] = (0, 0, 0)
    np.write()

def binary_index_blink():
    maxlen = math.ceil(math.log(lights, 2))
    for x in range(0, maxlen):  # for each possible binary digit
        for i in range(0, lights):  # for each pixel
            np[i] = (level, 0, 0)
            b = bin(i)[2:]  # drop first 2 char

            if x >= len(b):
                np[i] = (0, 0, 0)
            else:
                if b[x] == '1':
                    np[i] = (0, level, 0)
        np.write()
        time.sleep_ms(1000)
        allOff()
        time.sleep_ms(20)

def new_star(star = {}):
    star["pos"] = 0
    star["strip"] = strip[random(2) -1]
    star["color"] = pallet[random(len(pallet)-1)]
    star["speed"] = random(10)/5 + 0.25

    return star

def falling_stars():
    stars = []
    for i in range(0,5):
        star={}
        stars.append( new_star(star) )

    while keep_running():

        # turn all off, but don't write yet
        for i in range(0, np.n):
            np[i] = (0, 0, 0)
            
        for star in stars:
            strip = star['strip']
            pos = int(star['pos'])

            pixel = strip[pos]
            np[pixel] = star['color']

            star["pos"] += star["speed"]

            pos = int(star['pos'])
            if (pos >= len(strip)):
                star = new_star(star)

        np.write()
        # time.sleep(0.1)
        

## MAIN MAIN MAIN

allOff()

while keep_running():
    # binary_index_blink()
    falling_stars()
    if time.time() > 30:
        machine.reset()
