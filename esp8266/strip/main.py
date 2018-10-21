""" LED Strip Control

Control led lights based on MQTT messages
"""
import machine
import math
import neopixel
import network
import time
import ubinascii
import uos

from umqtt.simple import MQTTClient

pin = 4
topic = 'leds'
broker = 'jarvis'
lights = 150
segment_map = [0] * lights
np = neopixel.NeoPixel(machine.Pin(pin), lights)
client_id = 'esp8266_'+str(ubinascii.hexlify(machine.unique_id()), 'utf-8')
print("client_id = "+client_id)
topic = 'leds/' + client_id
client = MQTTClient(topic, broker)
print("listening to ", broker, " for ", topic)

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
    for i in range(0, 10):
        print(i)
        set_char(str(i))
        time.sleep_ms(750)
        set_binary(0)
        time.sleep_ms(250)


def pixel_or(i, a):
    """ apply or operation to a pixel_or
    i : index of pixel
    a : [r, g, b] array to apply
    """
    np[i] = (
        np[i][0] | a[0],
        np[i][1] | a[1],
        np[i][2] | a[2])


def test_rgb(t):
    for i in range(0, t):
        color = [
            (255, 255, 255),  # white
            (255, 0, 0),      # red
            (0, 255, 0),      # green
            (0, 0, 255)]      # blue
        for c in color:
            for x in range(0, 5):
                for j in range(0, lights):
                    if (j % 5) == x:
                        np[j] = c
                np.write()
                time.sleep(1)
            allOff()


def test_trains(t):
    """ RGB trains running around the strip
    """
    for i in range(0, t):
        # white train
        j = i % lights
        pixel_or(j, [255, 255, 255])
        np[(j - 10) % lights] = [0, 0, 0]

        # blue train
        j = int(i / 3) % lights
        pixel_or(j, [0, 0, 255])
        np[(j - 10) % lights] = [0, 0, 0]

        # green
        j = -i % lights
        pixel_or(j, [0, 255, 0])
        np[(j + 10) % lights] = [0, 0, 0]

        # green
        j = int(-i / 3) % lights
        pixel_or(j, [255, 0, 0])
        np[(j + 10) % lights] = [0, 0, 0]

        np.write()


def party():
    """ Show a lot of colors and animation
    """
    print("Party")
    for i in range(0, np.n):
        np[i] = (uos.urandom(1)[0], uos.urandom(1)[0], uos.urandom(1)[0])

    np.write()


def set_binary(b):
    """ Set calculated segments based on binary input

    Mapping is "Every pixel in the strip mapped to binary segment numbers"
    (Plural NUMBERS is key)
    """
    # points on the 7 segment display, each corner and middle endpoint
    endpoint = [0, 21, 42, 63, 84, 105, 126, 150]
    endpoint = [
        [21, 42],
        [0, 12],
        [105, 126],
        [84, 105],
        [63, 84],
        [42, 63],
        [125, 150]]

    # map the segments to pixels
    for s in range(0, 7):
        for i in range(endpoint[s][0], endpoint[s][1]):
            segment_map[i] = segment_map[i] | pow(2, s)

    for i in range(0, len(segment_map)):
        if (b & segment_map[i]):
            np[i] = (10, 10, 10)
        else:
            np[i] = (0, 0, 0)

    np.write()


def set_digit(d):
    """ set a digit 0-9
    """
    if d == 0:
        b = 1 | 2 | 4 | 16 | 32 | 64
    elif d == 1:
        b = 4 | 64
    elif d == 2:
        b = 2 | 4 | 8 | 16 | 32
    elif d == 3:
        b = 2 | 4 | 8 | 64 | 32
    elif d == 4:
        b = 1 | 4 | 8 | 64
    elif d == 5:
        b = 1 | 2 | 8 | 32 | 64
    elif d == 6:
        b = 1 | 2 | 8 | 16 | 32 | 64
    elif d == 7:
        b = 2 | 4 | 64
    elif d == 8:
        b = 1 | 2 | 4 | 8 | 16 | 32 | 64
    elif d == 9:
        b = 1 | 2 | 4 | 8 | 64

    set_binary(b)


def set_char(c):
    """ Char -> 7 segment mappings """
    # todo move this and other declarations to global space
    m = {
        '0': 0x3F, '1': 0x06, '2': 0x5B, '3': 0x4F, '4': 0x66, '5': 0x6D,
        '6': 0x7D, '7': 0x07, '8': 0x7F, '9': 0x6F, 'A': 0x77, 'b': 0x7C,
        'C': 0x39, 'd': 0x5E, 'E': 0x79, 'F': 0x71}

    set_binary(m[c])


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


def night_rider_2(l):
    """ Night rider red wave animation
    based on sin function
    """

    periods = 8

    for t in range(0, l):
        for p in range(0, np.n):

            f = t * 1.5

            v1 = math.cos(f / periods + p/2) - 0.7
            v1 = max(0, v1)

            v2 = math.cos(-f / periods + p/2) - 0.7
            v2 = max(0, v2)

            r = int(v1 * 50) + int(v2 * 50)

            np[p] = (r, 0, 0)

        np.write()
        time.sleep_ms(10)


def haloween(s):
    purple = [64, 0, 64]
    oragne = [64, 19, 0]

    for i in range(0, s):
            for p in range(0, np.n):
                if ((p + i) % 9) == 0:
                    np[p] = oragne
                elif ((p + i) % 22) == 0:
                    np[p] = purple
                else:
                    np[p] = [0, 0, 0]

            np.write()
            time.sleep(1)


def gotMessage(topic, msg):
    print(topic)
    print(msg)

    # Address single light via topc - disabled
    # light = int(topic.decode("utf-8").split('/')[-1])
    s_msg = msg.decode("utf-8")

    print("Got message ", msg)
    command = s_msg.split(' ')[0]
    payload = s_msg.split(' ')[1]

    print("Command ", command, "Paylod ", payload)

    if command == "b":
        i = int(payload)
        set_binary(i)

    if command == "d":
        d = int(payload)
        set_digit(d)

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
while True:
    test_rgb(10)
    test_trains(1000000)
    startUpAllOn()
    haloween(10)
    #night_rider_2(100)

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

# client.subscribe(b"strip/anet")
client.subscribe(topic)

while True:
    client.wait_msg()
