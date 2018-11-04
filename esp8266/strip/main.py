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
segment = [0] * 7
segment_map = [0] * lights
np = neopixel.NeoPixel(machine.Pin(pin), lights)
client_id = 'esp8266_'+str(ubinascii.hexlify(machine.unique_id()), 'utf-8')
print("client_id = "+client_id)
topic = 'leds/' + client_id
client = MQTTClient(topic, broker)
print("listening to ", broker, " for ", topic)

# points on the 7 segment display, each corner and middle endpoint
"""
endpoint = [
    [21, 42],
    [0, 21],
    [105, 126],
    [84, 105],
    [63, 84],
    [42, 63],
    [125, 150]]
"""

haloween_pallet = [
    (255, 140, 0),  # orange
    (255, 0, 255),  # purple
    (0, 255, 0),    # green
]

christmas_pallet = [
    (255, 0, 0),  # red
    (0, 255, 0),  # green
]

fall_pallet = [
    (255, 0, 0),  # red
    (0, 255, 0),  # green
    (255, 255, 0),  # yellow
    (255, 140, 0),  # orange
     ]

all_pallet = [
    (255, 0, 0),  # red
    (0, 255, 0),  # green
    (0, 0, 255),  # blue,
    (255, 255, 0),  # yellow
    (255, 0, 255),  # purple
    (0, 255, 255),
    (255, 140, 0),  # orange
     ]  # purple

pallet = fall_pallet


def setup_device():
    """ Configure installed device
    Based on client_id setup the pixel mapping etc
    points on the 7 segment display, each corner and middle endpoint
    See diagram for order of segments
    https://en.wikipedia.org/wiki/Seven-segment_display
    """
    global lights, segment
    if client_id == "esp8266_8b0e1200":
        publish("Config 3x5 test device")
        lights = 21
        segment[0] = [i for i in range(2, 6)]    # a
        segment[1] = [i for i in range(5, 9)]    # b
        segment[2] = [i for i in range(17, 20)] + [8]  # c
        segment[3] = [i for i in range(14, 18)]  # d
        segment[4] = [i for i in range(11, 15)]  # e
        segment[5] = [i for i in range(0, 3)]   # f
        segment[6] = [i for i in range(8, 12)]  # g


def allOff():
    """ Turn all the lights off
    """
    publish("allOff")
    for i in range(0, np.n):
        np[i] = (0, 0, 0)
    np.write()


def test_segments():
    """ test segment setup
    """
    publish("Test Segments")
    for i in range(0, 7):
        set_binary(pow(2, i))
        time.sleep_ms(100)
        set_binary(0)


def test_digits():
    """ Run through 0->9
    """
    publish("Test Digits")
    for i in range(0, 10):
        print(i)
        set_char(str(i))
        time.sleep_ms(750)
        set_binary(0)
        time.sleep_ms(250)


def party():
    """ Show a lot of colors and animation
    """
    publish("Party")
    for i in range(0, np.n):
        np[i] = (uos.urandom(1)[0], uos.urandom(1)[0], uos.urandom(1)[0])

    np.write()


def set_binary(b):
    """ Set calculated segments based on binary input

    segment[] describes the each segment
    segment_map[] maps each pixel to binary representation of segments it's in
    """

    # map the segments to pixels
    for s in range(0, 7):
        for i in segment[s]:
            segment_map[i] = segment_map[i] | pow(2, s)

    for i in range(0, len(segment_map)):
        if (b & segment_map[i]):
            np[i] = (10, 10, 10)
        else:
            np[i] = (0, 0, 0)

    np.write()


def set_char(c):
    """ Char -> 7 segment mappings """
    # todo move this and other declarations to global space
    # https://en.wikipedia.org/wiki/Seven-segment_display#Displaying_letters

    m = {
        '0': 0x3F, '1': 0x06, '2': 0x5B, '3': 0x4F, '4': 0x66, '5': 0x6D,
        '6': 0x7D, '7': 0x07, '8': 0x7F, '9': 0x6F, 'A': 0x77, 'b': 0x7C,
        'C': 0x39, 'd': 0x5E, 'E': 0x79, 'F': 0x71}

    set_binary(m[c])


def random_star():
    star = {}
    star['pixel'] = int((lights-1) * uos.urandom(1)[0] / 255)
    star['color'] = pallet[int(len(pallet) * uos.urandom(1)[0] / 256)]
    star['speed'] = uos.urandom(1)[0] / 256
    return star


def twinkle(t):
    """ twikling star pattern
    """
    publish("twinkle")

    starfield = []
    for i in range(0, 10):
        starfield.append(random_star())

    for i in range(0, t * 20):
        client.check_msg()
        for star in starfield:
            r = star['color'][0]
            g = star['color'][1]
            b = star['color'][2]
            r = int(r * star['speed'])
            g = int(g * star['speed'])
            b = int(b * star['speed'])
            new_color = (r, g, b)
            star['color'] = new_color
            np[star['pixel']] = star['color']

            if (r+g+b) == 0:
                starfield.remove(star)
                starfield.append(random_star())

        np.write()
        time.sleep_ms(50)


def random_flake():
    """ Initialize a snow flake
    """
    flake = {}

    # Either left or right side of window
    if uos.urandom(1)[0] > 128:
        flake['path'] = segment[1] + segment[2]
    else:
        flake['path'] = segment[5] + segment[4]

    flake['pos'] = 0
    return flake


def snow(t):
    """ using segments A B and F E, show snow falling
    """
    publish("snow")

    storm = []
    for i in range(0, 1):
        storm.append(random_flake())

    for i in range(0, t):
        for flake in storm:
            print(flake['path'])

            pos = flake['pos']

            pixel = flake['path'][pos]
            print("pixel = off", pixel)

            # clear prev pixel
            np[flake['path'][pos]] = [0, 0, 0]

            flake['pos'] += 1

            if flake['pos'] >= len(flake['path']):
                storm.remove(flake)
                storm.append(random_flake())
            else:
                pixel = flake['path'][pos]
                print("pixel ON= ", pixel)

                np[pixel] = [25, 25, 25]

        np.write()
        time.sleep_ms(50)


def binary_index_blink(t):
    """ binary_index_blink
    blink the binary red/green pattern of each pixels index
    """
    maxlen = round(math.log(lights, 2))
    for x in range(0, maxlen):  # for each possible binary digit
        for i in range(0, lights):  # for each pixel
            np[i] = (10, 0, 0)
            b = bin(i)[2:]  # drop first 2 char

            print("x=" + str(x) + " b=" + b)

            if x >= len(b):
                np[i] = (0, 0, 0)
            else:
                if b[x] == '1':
                    np[i] = (0, 10, 0)
        np.write()
        time.sleep_ms(10)
        allOff()
        time.sleep_ms(10)



def frangable_publish(topic, payload):
    """If power goes out - we may try to log before homeassistant is back
    so if we fail - sleep a bit and try to reconnect the mqtt client
    drop current message on the floor
    """
    try:
        client.publish(topic, payload)
        print("Wrote", payload, " to ", topic)
    except:
        print("failed to log, sleeping 1")
        time.sleep(1)
        try:
            client.connect()
        except:
            print("failed to connect")


def publish(message):
    """ publish to topic containing device_id
    """
    print(message)
    frangable_publish("/strip/health/" + client_id, message)


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
        test_digits()

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

setup_device()

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
publish("alive")

# client.subscribe(b"strip/anet")
client.set_callback(gotMessage)
client.subscribe(topic)

allOff()

while True:
    binary_index_blink(100)
    # morse(100)
    # snow(1000)
    # twinkle(10)
    # test_rgb(1)
    # test_trains(300)
    # test_digits()
    test_segments()
    # party()
