import machine
import math
import neopixel
import network
import ntptime
import time
import ubinascii
import uos
from umqtt.simple import MQTTClient

motd = "2018-11-17 Suzy wants Yellow and Red"

pin = 4
topic = 'leds'
broker = 'jarvis'
lights = 150
brightness = 255

segment = [[0]] * 7
for i in range(0, 7):
    segment[i] = [x for x in range(i * 21, (i+1)*21)]

segment_map = [0] * lights
np = neopixel.NeoPixel(machine.Pin(pin), lights)
client_id = 'esp8266_'+str(ubinascii.hexlify(machine.unique_id()), 'utf-8')
print("client_id = "+client_id)
topic = 'leds/' + client_id
client = MQTTClient(topic, broker)
print("listening to ", broker, " for ", topic)

pallet = [
    (255, 0, 0),      # red
    # (0, 255, 0),      # green
    (50, 155, 0),    # yellow
    # (170, 255, 0),    # orange
    # (0, 0, 255),      # blue
    # (255, 255, 255),  # white
     ]


def setup_device():
    return
    global lights, segment
    if client_id == "esp8266_8b0e1200":
        publish("Config 3x5 test device")
        lights = 21
        segment[0] = [i for i in range(2, 6)]    # a
        segment[1] = [i for i in range(5, 9)]    # b
        segment[2] = [i for i in range(17, 20)] + [8]  # c
        segment[3] = [i for i in range(14, 18)]  # d
        segment[4] = [i for i in range(11, 15)]  # e
        segment[5] = [i for i in range(0, 3)] + [11]   # f
        segment[6] = [i for i in range(8, 12)]  # g

    if client_id == "esp8266_609a1100":
        publish("Config window 1")
        lights = 150
        segment[0] = [i for i in range(22, 48)]    # a
        segment[1] = [i for i in range(48, 71)]    # b
        segment[2] = [i for i in range(71, 93)]  # c
        segment[3] = [i for i in range(93, 120)]  # d
        segment[4] = [i for i in range(120, 145)]  # e
        segment[5] = [i for i in range(0, 22)]   # f
        segment[6] = [i for i in range(145, 150)]  # g

    if client_id == "esp8266_8f141200":
        publish("Confic 4x8 test device")
        lights = 24
        segment[0] = [i for i in range(13, 18)]    # a
        segment[1] = [i for i in range(17, 22)]    # b
        segment[2] = [21] + [i for i in range(0, 3)]  # c
        segment[3] = [i for i in range(2, 8)]  # d
        segment[4] = [i for i in range(6, 11)]  # e
        segment[5] = [i for i in range(10, 15)]   # f
        segment[6] = [i for i in range(21, 27)] + [10]  # g


def allOff():
    for i in range(0, np.n):
        np[i] = (0, 0, 0)
    np.write()


def time_check():
    publish("time check")

    try:
        ntptime.settime()
        if (time.localtime()[3] - 5) % 24 >= 23:
            publish("sleeping for 8hr")
            for h in range(0, 8):
                print("sleep an hour")
                time.sleep(60 * 60)
    except:
        print(".")


def test_segments():
    publish("Test Segments")
    for i in range(0, 7):
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
    publish("pallet complete")
    c = pallet[int(len(pallet) * uos.urandom(1)[0] / 256)]
    for i in range(0, t * 20):
        client.check_msg()
        for p in range(0, lights):
            np[p] = c
        np.write()
    time.sleep(1)


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



def frangable_publish(topic, payload):
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
    frangable_publish("/strip/health/" + client_id, message)


def gotMessage(topic, msg):
    # s_msg = msg.decode("utf-8")
    publish("resetting in 1 second")
    time.sleep(1)
    machine.reset()


setup_device()

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
client.subscribe(topic)

allOff()

while True:
    time_check()
    cycle_pallet(1)
    # binary_index_blink(100)
    # snow(1000)
    # twinkle(30)
    # test_digits()
    # test_segments()
