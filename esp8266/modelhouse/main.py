""" Model House Light Control

Control led lights in model house based on MQTT messages
"""
import machine
import neopixel
import network
import time
import uos

from umqtt.simple import MQTTClient

topic = 'model'
broker = '192.168.1.117' #'jarvis'
client= MQTTClient('model', broker)

np = neopixel.NeoPixel(machine.Pin(4), 6)


def cycle(iterations, speed):
    for i in range(0, iterations):
        for i in range(0, np.n):
            np[(i-1) % np.n] = (0, 0, 0)
            np[i] = (10, 10, 10)
            np.write()
            time.sleep_ms(speed)


def diagnostic():

    n = np.n
    print("Count = ", n)

    cycle(3, 1000)
    cycle(10, 100)
    cycle(10, 50)
    cycle(10, 30)

    for j in range(0, 40):
        for i in range(0, n):
            r = 10
            if uos.urandom(1) <= b'\x30':
                r = 255

            np[(i-1) % n] = (0, 0, 0)
            np[i] = (r, 10, 10)
            np.write()

            time.sleep_ms(30)

    for j in range(255, 0, -5):
        for i in range(0, n):
            np[i] = (j, 0, 0)
            np.write()
            time.sleep_ms(10)


def party():
    n = np.n

    # Drums
    for i in range(80):
        if not (i % 4):
            np[0] = (5, 5, 5)
        else:
            np[0] = (0, 0, 0)

        if not(i % 16):
            np[3] = (255, 0, 255)
        else:
            np[3] = (0, 0, 0)

        np.write()
        time.sleep_ms(100)

    # cycle
    for i in range(12 * n):  # was 4
        for j in range(n):
            np[j] = (0, 0, 0)
        np[i % n] = (255, 255, 255)
        np.write()
        time.sleep_ms(25)

    # bounce
    for i in range(4 * n):
        for j in range(n):
            np[j] = (0, 0, 128)
        if (i // n) % 2 == 0:
            np[i % n] = (0, 0, 0)
        else:
            np[n - 1 - (i % n)] = (0, 0, 0)
        np.write()
        time.sleep_ms(60)

    # fade in/out
    for i in range(0, 4 * 256, 8):
        for j in range(n):
            if (i // 256) % 2 == 0:
                val = i & 0xff
            else:
                val = 255 - (i & 0xff)
            np[j] = (val, 0, 0)
        np.write()

    # clear
    for i in range(n):
        np[i] = (0, 0, 0)
    np.write()


def gotMessage(topic, msg):
    print(topic)
    print(msg)

    light = int(topic.decode("utf-8").split('/')[-1])

    if msg == b'on':
        np[light] = (10, 10, 10)
        np.write()
        print("Turn On")

    if msg == b'off':
        np[light] = (0, 0, 0)
        np.write()
        print("Turn Off")

    if msg == b'party':
        party()
        print("Party")


client.set_callback(gotMessage)

diagnostic()

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

client.subscribe(b"model/light/#")

party(np)
while True:

    client.wait_msg()

    print("Waiting")
    time.sleep(1)
