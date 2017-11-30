""" Furnace vibration minion

Measure accelerometer movement and log time the furnace is on
"""

from machine import I2C, Pin
import time

import homeassistant
import morsecode

SENSITIVITY = 5
LOOP_SLEEP = 0.1

# connect to the world
hass = homeassistant.HomeAssistant('http://jarvis:8123', 'suzymatt')

# create i2c object to talk to accelerometer
i2c = I2C(freq=400000, scl=Pin(5), sda=Pin(4))

# activate accelerometer
i2c.writeto_mem(29, 0x2a, b'\x01')

x = y = z = 0

# are we currently vibrating
v = False
start = time.time()

led = Pin(2, Pin.OUT)

while True:
    # read 6 char from the accelerometer
    r = i2c.readfrom_mem(29, 0x01, 6)

    # Calculate diff from last readings
    xd = x - r[0]
    yd = y - r[2]
    zd = z - r[4]

    # Remember readings
    x = r[0]
    y = r[2]
    z = r[4]

    # might need some better math her to calc 255->0 correctly
    total = abs(xd) + abs(yd) + abs(zd)

    # are we vibrating?
    if (total > SENSITIVITY):
        # is this a new state
        if not v:
            v = True
            start = time.time()
            led.low()
    else:
        if v:
            v = False
            timespan = time.time() - start
            print("time = ", timespan)
            led.high()

    time.sleep(LOOP_SLEEP)
