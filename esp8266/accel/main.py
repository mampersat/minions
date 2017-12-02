""" Furnace vibration minion

Measure accelerometer movement and log time the furnace is on
"""

from machine import I2C, Pin
import time

import homeassistant
import morsecode


print("Running")

# Fucked around with a 20 SENSITIVITY prev
SENSITIVITY = 5
LOOP_SLEEP = 0.1

# connect to the world
hass = homeassistant.HomeAssistant('http://jarvis:8123', 'suzymatt')

# create i2c object to talk to accelerometer
i2c = I2C(freq=400000, scl=Pin(5), sda=Pin(4))

# activate accelerometer
i2c.writeto_mem(29, 0x2a, b'\x01')

# are we currently vibrating
recording = False
start = time.time()

led = Pin(2, Pin.OUT)


def listen_for_a_sec():
    """Ping 10 times in a second for motion, return true if detected
    """
    ret = False
    x = y = z = 0
    for t in range(0, 10):

        r = i2c.readfrom_mem(29, 0x01, 6)

        # Calculate diff from last readings
        xd = abs(abs(x - 128) - abs(r[0] - 128))
        yd = abs(abs(y - 128) - abs(r[2] - 128))
        zd = abs(abs(z - 128) - abs(r[4] - 128))

        # Remember readings
        x = r[0]
        y = r[2]
        z = r[4]

        # might need some better math her to calc 255->0 correctly
        total = xd + yd + zd

        print(total)

        # are we vibrating?
        if (total > SENSITIVITY) and (t > 0):
            ret = True

        time.sleep(LOOP_SLEEP)

    print("Listen resutl = ", ret)
    return ret


while True:
    print("while true loop")
    if listen_for_a_sec():
        led.low()
        if not recording:
            start = time.time()
            recodring = True
    else:
        led.high()
        if recording:
            recording = False
            timespan = time.time() - start
            print(timespan)
