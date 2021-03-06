import machine
import math
import neopixel
import network
import time
import ubinascii
import uos # random numbers
from umqtt.simple import MQTTClient

motd = "09-03:1"

pin = 14
topic = 'leds'
broker = 'jarvis'
lights = 150
level = 127
mode = "ho"


np = neopixel.NeoPixel(machine.Pin(pin), lights)
nps = {}

client_id = 'esp8266_'+str(ubinascii.hexlify(machine.unique_id()), 'utf-8')
print("client_id = "+client_id)
topic = 'leds/' + client_id

fleet = {}
fleet['esp8266_8f141200'] = "2 H HHH    d L " #  1
fleet['esp8266_8b0e1200'] = "0 O OOO  1 A E " #  2
fleet['esp8266_5133d500'] = "1 H HHH    Y F " #  4
fleet['esp8266_51333700'] = "8 O OOO      T " #  5
fleet['esp8266_609a1100'] = "8               " #  6
fleet['esp8266_7f35d500'] = "8 8 8 8 8 8 8 8" #  5x8
fleet['esp8266_c1584a00'] = "8 8 8 8 8 8 8 8"  #  3x5

segment = [[0]] * 7
for i in range(0, 7):
    j = (1, 2, 3, 4, 5, 0, 6)[i]
    if client_id == "esp8266_5133d500":
        # publish("I'm special")
        j = (5, 4, 3, 2, 1, 6, 0)[i]
    segment[i] = [x for x in range(j * 21, (j+1)*21)]
segment_map = [0] * lights
display_char = last_display_char = 0

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
    'F': 113, 'L': 56, 'H': 118, 'D': 99,
    'O': 0x3F, 'T' : 120, ' ': 0}


def allOff():
    for i in range(0, np.n):
        np[i] = (0, 0, 0)
    np.write()


def test_segments():
    publish("Test Segments")
    for i in range(0, 7):
        set_binary(pow(2, i))
        time.sleep_ms(100)
        set_binary(0)


def set_binary(b, neo = np):
    # map the segments to pixels
    for s in range(0, 7):
        for i in segment[s]:
            segment_map[i] = segment_map[i] | pow(2, s)

    for i in range(0, len(segment_map)):
        if (b & segment_map[i]):
            # np[i] = pallet[int(len(pallet) * uos.urandom(1)[0] / 256)]
            neo[i] = (255, 255, 255)
        else:
            neo[i] = (0, 0, 0)

    np.write()


def set_char(c, neo = np):
    # publish("set char: " + c)
    global char_segment_map
    if c in char_segment_map:
        set_binary(char_segment_map[c], neo)


def cycle_char():
    for c in char_segment_map:
        print(c)
        set_char(c)
        time.sleep(1)


def cycle_pallet(t):
    publish("spin pallet")
    c = pallet[int(len(pallet) * uos.urandom(1)[0] / 256)]
    d = (int(c[0] / 5), int(c[1] / 5), int(c[2] / 5))

    for j in range(0, t):
            for on in range(j, lights + j, 44):
                c = pallet[int(len(pallet) * uos.urandom(1)[0] / 256)]
                d = (int(c[0] / 5), int(c[1] / 5), int(c[2] / 5))

                dim = (on - 1) % lights
                off = (on - 2) % lights
                np[on % lights] = c
                np[dim] = d
                np[off] = (0, 0, 0)
            np.write()
            time.sleep_ms(300)

def onestar(t):
    publish("onestar")
    
    for j in range(0, t):
        i = int(lights * uos.urandom(1)[0] / 256)
        for l in range(120, -1, -1):
            # print("i = ", i, " l = ", l)
            np[i] = (l, l, l)
            np.write()
            # time.sleep_ms(10)
    
def ho():
    global display_char, last_display_char

    if display_char != last_display_char:
        nps[display_char % len(nps)].write()
        last_display_char = display_char
        publish("ho " + str(display_char))

    # time.sleep_ms(100)


def binary_index_blink(t):
    publish("binary index blink")
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
        time.sleep_ms(20)
        allOff()
        time.sleep_ms(10)


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
    frangable_publish("/strip/health/" + client_id, motd + ":" + message)


def gotMessage(topic, msg):
    global display_char, mode
    s_msg = msg.decode("utf-8")
    publish("got msg: " + s_msg)
    if s_msg == "b":
        publish("resetting")
        allOff()
        machine.reset()
    if s_msg == "s":
        mode = "sleep"
    if s_msg == "cycle":
        mode = "cycle"
    if s_msg == "ho":
        mode = "ho"
    if s_msg[0] == "m":
        display_char = int(msg[1:])


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


## MAIN MAIN MAIN

while True:
    # onestar(30)
    # binary_index_blink(1)
    cycle_pallet(20)
    time.sleep(5)

letters = "        "
if client_id in fleet:
    letters = fleet[client_id]

for i in range(0, len(letters)):
    nps[i] = neopixel.NeoPixel(machine.Pin(4), lights)
    set_char(letters[i], nps[i])

client.set_callback(gotMessage)
client.subscribe("/strip/command/" + client_id)

allOff()

while True:
    client.check_msg()
    if mode == "sleep":
        allOff()
        time.sleep(1)
    if mode == "cycle":
        cycle_pallet(15)
    if mode == "ho":
        ho()
    if mode == "test":
        test(1)
