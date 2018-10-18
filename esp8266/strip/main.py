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
lights = 32
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


def set_binary(b):
    """ Set calculated segments based on binary input

    Mapping is "Every pixel in the strip mapped to binary segment numbers"
    (Plural NUMBERS is key)
    """
    segment_map = [0, 1, 3, 0,
                   2, 6, 0,
                   4, 76, 0,
                   8, 25, 0,
                   16, 48, 0,
                   32, 96, 0,
                   64]

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

    periods = 8

    for t in range(0, 1000000):
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

# client.subscribe(b"strip/anet")
client.subscribe(topic)

while True:
    client.wait_msg()
