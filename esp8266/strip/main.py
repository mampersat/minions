import machine
import math
import neopixel
import network
import time
import ubinascii
import uos
from umqtt.simple import MQTTClient

motd = "2018-11-25 Recusion avoidance"

topic = 'leds'
broker = 'jarvis'
lights = 150
brightness = 255

np = neopixel.NeoPixel(machine.Pin(4), lights)
client_id = 'esp8266_'+str(ubinascii.hexlify(machine.unique_id()), 'utf-8')
print("client_id = "+client_id)
topic = 'leds/' + client_id

segment = [[0]] * 7
for i in range(0, 7):
    j = (1, 2, 3, 4, 5, 0, 6)[i]
    if client_id == "esp8266_5133d500":
        # publish("I'm special")
        j = (5, 4, 3, 2, 1, 6, 0)[i]
    segment[i] = [x for x in range(j * 21, (j+1)*21)]
segment_map = [0] * lights
display_char = ''

client = MQTTClient(topic, broker)
print("listening to ", broker, " for ", topic)

pallet = [
    (255, 0, 0),      # red
    (0, 255, 0),      # green
    (70, 105, 0),    # yellow
    (170, 255, 0),    # orange
    (0, 0, 255),      # blue
    # (255, 255, 255),  # white
     ]

char_segment_map = {
    '0': 0x3F, '1': 0x06, '2': 0x5B, '3': 0x4F, '4': 0x66, '5': 0x6D,
    '6': 0x7D, '7': 0x07, '8': 0x7F, '9': 0x6F, 'A': 0x77, 'b': 0x7C,
    'C': 0x39, 'd': 0x5E, 'E': 0x79, 'F': 0x71,
    'N': 55, 'S': 109, 'U': 62, 'Z': 91, 'Y': 110,
    'F': 113, 'L': 56, 'H': 118, 'D': 99}


def allOff():
    for i in range(0, np.n):
        np[i] = (0, 0, 0)
    np.write()


def test_segments():
    publish("Test Segments")
    for i in range(0, 7):
        client.check_msg()
        set_binary(pow(2, i))
        time.sleep_ms(100)
        set_binary(0)


def set_binary(b):

    # map the segments to pixels
    for s in range(0, 7):
        for i in segment[s]:
            segment_map[i] = segment_map[i] | pow(2, s)

    for i in range(0, len(segment_map)):
        if (b & segment_map[i]):
            np[i] = (brightness, brightness, brightness)
        else:
            np[i] = (0, 0, 0)

    np.write()


def set_char(c):
    publish("set char: " + c)
    global char_segment_map

    set_binary(char_segment_map[c])
    time.sleep(1)


def cycle_char():
    for c in char_segment_map:
        print(c)
        set_char(c)
        time.sleep(1)


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
    for i in range(0, 30):
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
        time.sleep_ms(100)
    allOff()


def cycle_pallet(t):
    publish("spin pallet")
    c = pallet[int(len(pallet) * uos.urandom(1)[0] / 256)]
    d = (int(c[0] / 5), int(c[1] / 5), int(c[2] / 5))

    for j in range(0, t):
            for on in range(j, lights + j, 10):
                c = pallet[int(len(pallet) * uos.urandom(1)[0] / 256)]
                d = (int(c[0] / 5), int(c[1] / 5), int(c[2] / 5))

                client.check_msg()
                dim = (on - 1) % lights
                off = (on - 2) % lights
                np[on % lights] = c
                np[dim] = d
                np[off] = (0, 0, 0)
            np.write()
            time.sleep_ms(100)


def binary_index_blink(t):
    publish("binary index blink")
    maxlen = math.ceil(math.log(lights, 2))
    for x in range(0, maxlen):  # for each possible binary digit
        for i in range(0, lights):  # for each pixel
            np[i] = (255, 0, 0)
            b = bin(i)[2:]  # drop first 2 char

            if x >= len(b):
                np[i] = (0, 0, 0)
            else:
                if b[x] == '1':
                    np[i] = (0, 255, 0)
        np.write()
        time.sleep_ms(20)
        allOff()
        time.sleep_ms(10)


def sleep():
    publish("Sleeping")
    allOff()
    while True:
        client.check_msg()
        time.sleep(1)


def frangable_publish(topic, payload):
    try:
        client.publish(topic, payload)
        print("Wrote", payload, " to ", topic)
    except:
        print("failed to log, sleeping - dropping")
        time.sleep(1)
        #try:
        #    client.connect()
        #except:
        #    print("failed to connect")


def publish(message):
    frangable_publish("/strip/health/" + client_id, message)


def gotMessage(topic, msg):
    global display_char
    s_msg = msg.decode("utf-8")
    publish("got msg: " + s_msg)
    if s_msg == "b":
        publish("resetting")
        allOff()
        machine.reset()
    if s_msg == "s":
        sleep()
    if s_msg[0] == 'l':
        display_char = s_msg[1]
    if s_msg[0] == 'c':
        display_char = ''


s = network.WLAN(network.STA_IF)
while not s.isconnected():
    publish("Network not connected - sleeping")
    time.sleep(1)

print(s.ifconfig())

connected = False
while not connected:
    try:
        client.connect()
    except:
        print(".")
        time.sleep(1)
    else:
        connected = True
publish("alive " + motd + ' ' + s.ifconfig()[0])

client.set_callback(gotMessage)
client.subscribe("/strip/command/" + client_id)

allOff()

while True:
    client.check_msg()
    if display_char == '':
        cycle_pallet(50)
        # binary_index_blink(100)
        # twinkle(30)
        # test_digits()
        # test_segments()
    else:
        set_char(display_char)
