import machine
import math
import neopixel
import network
import time
import ubinascii
import uos  # random numbers
import utime
import config
from umqtt.simple import MQTTClient

pin = 14
topic = 'leds'
broker = 'jarvis'
lights = 150
level = 10
mode = "ho"

np = neopixel.NeoPixel(machine.Pin(pin), lights)

# fall
pallet = [
    (100, 0, 0),      # red
    (0, 100, 0),      # green
    (100, 100, 0),    # yellow
    (100, 50, 0),    # orange
]


def random(i):
    if i:
        return int(uos.urandom(1)[0]/256 * i)
    else:
        return uos.urandom(1)[0]/256


def keep_running():
    if utime.ticks_ms() < 50000:  # about 30s
        return True
    else:
        publish("resetting")
        time.sleep(1)
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


def new_star(star={}):
    star["pos"] = 0
    star["strip"] = config.strip[random(2) - 1]
    star["color"] = pallet[random(len(pallet)-1)]
    star["speed"] = random(10)/5 + 0.25

    return star


def falling_stars():
    stars = []
    for i in range(0, 5):
        star = {}
        stars.append(new_star(star))

    while keep_running():

        # turn all off, but don't write yet
        for i in range(0, np.n):
            np[i] = (0, 0, 0)

        for star in stars:
            strip = star['strip']
            first = int(star['pos'])
            second = first +1
            first_percent = star['pos'] -first
            second_percent = 1 - first_percent

            pixel = strip[first]
            np[pixel] = (
                int( star['color'][0] * first_percent),
                int( star['color'][1] * first_percent),
                int( star['color'][2] * first_percent),
            )
            
            if (second < len(strip)) :
                pixel = strip[second]
                np[pixel] = (
                    int( star['color'][0] * second_percent),
                    int( star['color'][1] * second_percent),
                    int( star['color'][2] * second_percent),
                )
            star["pos"] += star["speed"]

            pos = int(star['pos'])
            if (pos >= len(strip)):
                star = new_star(star)

        np.write()
        # time.sleep(0.1)

version = '0.9.3'
client_id='esp8266_'+str(ubinascii.hexlify(machine.unique_id()), 'utf-8')
topic='leds/' + client_id
host='192.168.1.132'
client=MQTTClient(topic, host)



def frangable_publish(topic, payload):
    try:
        client.publish(topic, payload)
        print("Wrote", payload, " to ", topic)
    except:
        time.sleep(1)
        print("failed to log, took a nap")
        try:
            client.connect()
        except:
            print("failed to connect")


def publish(message):
    frangable_publish("/strip/health/" + client_id, version + ":" + message)

s = network.WLAN(network.STA_IF)
while not s.isconnected():
    publish("Network not connected - sleeping")
    time.sleep(1)

client.connect()

def gotMessage(topic, msg):
    s_msg = msg.decode("utf-8")
    publish("got msg: " + s_msg)
    if s_msg == "b":
        publish("resetting")
        allOff()
        machine.reset()

client.set_callback(gotMessage)
client.subscribe("/strip/command/" + client_id)

publish("hello")
# -------------------------------------------------------------------------------------------------------------------------

allOff()

while keep_running():
    # binary_index_blink()
    falling_stars()

