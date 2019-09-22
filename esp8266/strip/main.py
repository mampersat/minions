import machine
import math
import neopixel
import network
import os
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

np = neopixel.NeoPixel(machine.Pin(pin), lights)

np[0] = (0,10,0)
np.write()

# fall
pallet = [
    (100, 0, 0),      # red
    (0, 100, 0),      # green
    (100, 100, 0),    # yellow
    (100, 50, 0),    # orange
]


def random(i=1):
    if (i != 1):
        return int(uos.urandom(1)[0]/256 * i)
    else:
        return uos.urandom(1)[0]/256


def keep_running():
    client.check_msg()
    if utime.ticks_ms() < 100000:  # about 1m
        return True
    else:
        publish("reset")
        np[0] = (10,0,0)
        np.write()
        time.sleep(1)
        machine.reset()


"""
    ___          _                 __  _           
   /   |  ____  (_)___ ___  ____ _/ /_(_)___  ____ 
  / /| | / __ \/ / __ `__ \/ __ `/ __/ / __ \/ __ \
 / ___ |/ / / / / / / / / / /_/ / /_/ / /_/ / / / /
/_/  |_/_/ /_/_/_/ /_/ /_/\__,_/\__/_/\____/_/ /_/ 
"""

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
    for i in range(0, 3):
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
        time.sleep(0.5)

def party():
    for i in range(0, np.n):
        if (random(5)== 1):
            np[i] = (
                random(12),
                random(12),
                random(12)
            )
        else:
            np[i] = (0, 0, 0)
    np.write()

def new_twinkling_star(star={}):
    star['p'] = random(np.n)
    star['b'] = 50
    star['v'] = 0.9 + random() * 0.09
    return(star)

def twinkling_stars():
    
    stars=[]
    
    for i in range(0,3):
        star = {}
        star = new_twinkling_star(star)
        stars.append(star)
    
    while keep_running():
        for i in range(0, len(stars)):
            star = stars[i]
            star['b'] *= star['v']
            if star['b'] > 10:
                bright = int( star['b'])
                r = bright
                g = int(bright * 0.57)
                b = 0
                np[star['p']] = ( r, g, b)
            else:
                np[star['p']] = (0,0,0)
                star = new_twinkling_star(star)

        np.write()
        time.sleep_ms(30)

def sleeping():
    for b in range(0,100):
        np[0] = (0, 0, b)
        np.write()
        
    for b in range(100, 0, -1):
        np[0] = (0, 0, b)
        np.write()
        time.sleep_ms(20)

"""
            _                      _          _     _ _   
 _ __   ___| |___      _____  _ __| | __  ___| |__ (_) |_ 
| '_ \ / _ \ __\ \ /\ / / _ \| '__| |/ / / __| '_ \| | __|
| | | |  __/ |_ \ V  V / (_) | |  |   <  \__ \ | | | | |_ 
|_| |_|\___|\__| \_/\_/ \___/|_|  |_|\_\ |___/_| |_|_|\__|
"""                                                          

version = '0.17.0'
client_id='esp8266_'+str(ubinascii.hexlify(machine.unique_id()), 'utf-8')
topic='leds/' + client_id
host='192.168.1.132'
client=MQTTClient(topic, host)

state = sleeping

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

def set_state(new_state):
    global state
    
    if new_state == "sleep":
        state = sleeping
    if new_state == "twinkling_stars":
        state = twinkling_stars
    
    f = open('state.txt', 'w')
    f.write(new_state)
    f.close()
    print("wrote state: " + new_state)

def get_state():

    new_state="sleep"

    if 'state.txt' in os.listdir():
        f = open('state.txt')
        new_state = f.read()
        f.close()
    set_state(new_state)
    return(new_state)

def gotMessage(topic, msg):
    print("Got message")
    global state
    s_msg = msg.decode("utf-8")
    publish("got msg: " + s_msg)
    if s_msg == "b":
        publish("reset")
        allOff()
        time.sleep(2)
        machine.reset()
    else:
        set_state(s_msg)

client.connect()
client.set_callback(gotMessage)
listen_topic = "/strip/command/" + client_id
client.subscribe(listen_topic)
print("Listening to ", listen_topic)

cur_state = get_state()

publish("hello: " + cur_state)

"""
  _       __    _   _          _     ___   ___   ___  
 | |\/|  / /\  | | | |\ |     | |   / / \ / / \ | |_) 
 |_|  | /_/--\ |_| |_| \|     |_|__ \_\_/ \_\_/ |_|   
"""

allOff()

while keep_running():
    # binary_index_blink()
    # falling_stars()
    # party()
    # twinkling_stars()
    state()


