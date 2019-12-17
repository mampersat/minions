import machine
import math
import neopixel
import network
import time
import ubinascii
import uos  # random numbers
import utime
import urequests

pin = 14
topic = 'leds'
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
                random(210),
                random(210),
                random(210)
            )
        else:
            np[i] = (0, 0, 0)
    np.write()

def new_twinkling_star(star={}):
    star['p'] = random(np.n)
    star['b'] = 200
    star['v'] = 0.9 + random() * 0.09
    return(star)

def twinkling_stars():
    
    stars=[]
    
    for i in range(0,10):
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

def blue():
    for i in range(0, np.n):
        np[i] = (0, 0, int (math.cos(utime.ticks_ms() / 500) * 127 + 127))
    np.write()


def sleeping():

    # np[0] = (0, 0, int(utime.ticks_ms() / 10 % 255)
    i = int(utime.ticks_ms() / 1000 % 10)

    np[0] = (0, 0, i)

    np.write()

def time_calibration():
    i = int(time.time() % 10)
    np[i] = (0,100,0)
    np[(i-1) %10] = (0, 0, 0)
    np.write()
    # publish(str(time.time()))
    time.sleep_ms(250)

def orange():
    for i in range(0, np.n, 8):
        t = utime.ticks_ms() / 500 + (i/3.14)
        np[i] = (
            int (math.cos(t) * 127),
            int (math.cos(t) * 127),
            0)
    np.write()

def xmas():
    chunked_t = int(utime.ticks_ms() /1000)
    for i in range(1, 25):
        on = chunked_t * 29 * i
        off = (chunked_t-1) * 29 * i
        np[ on % np.n] = (100, 0 , 0)
        np[ off % np.n] = (0,0,0)

    for i in range(26, 31):
        on = chunked_t * 29 * i
        off = (chunked_t-1) * 29 * i
        np[ on % np.n] = (100, 100 , 100)
        np[ off % np.n] = (0,0,0)


    np.write()

def red_white():

    t = int(utime.ticks_ms() /1000)
    
    for i in range(0, np.n):

        thick = 6

        if ( (i +t) % thick <thick /2 ):
            np[i] = (100, 0, 0)
        else:
            np[i] = (0, 100, 0)

    np.write()
    
"""
            _                      _          _     _ _   
 _ __   ___| |___      _____  _ __| | __  ___| |__ (_) |_ 
| '_ \ / _ \ __\ \ /\ / / _ \| '__| |/ / / __| '_ \| | __|
| | | |  __/ |_ \ V  V / (_) | |  |   <  \__ \ | | | | |_ 
|_| |_|\___|\__| \_/\_/ \___/|_|  |_|\_\ |___/_| |_|_|\__|
"""                                                          

version = 10
client_id='esp8266_'+str(ubinascii.hexlify(machine.unique_id()), 'utf-8')

command = "red_white"
state = red_white

def set_state():
    global state
    if command == "orange":
        state = orange
    if command == "party":
        state = party
    if command == "sleep":
        state = sleeping
    if command == "blue":
        state = blue
    if command == "xmas":
        state = xmas


def get_command():
    global command
    global version
    
    print("Checking")

    s = network.WLAN(network.STA_IF)
    if s.isconnected():
        print("Connected - getting command")
        try:
            server_command = urequests.get('http://192.168.1.132:8000/command.html').text
            if (server_command != command):
                command = server_command
                allOff()
            print("Got command ", command)
            server_version = urequests.get('http://192.168.1.132:8000/version.html').text
            print("Got version ", server_version)
            if int(server_version) > version:
                machine.reset()
        except:
            print("Error getting command from server, defaulting to ", command)
        set_state()
    else:
        print("Not connected")

"""
  _       __    _   _          _     ___   ___   ___  
 | |\/|  / /\  | | | |\ |     | |   / / \ / / \ | |_) 
 |_|  | /_/--\ |_| |_| \|     |_|__ \_\_/ \_\_/ |_|   
"""

# give the device a few seconds to connect to WIFI
last_check_ms = -10000

def keep_running():
    global last_check_ms

    if utime.ticks_ms() > last_check_ms:
        last_check_ms = utime.ticks_ms() + 10000
        get_command()
    
    return True


allOff()

# while keep_running():

while True:
    state()