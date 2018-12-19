"""
main.py
measure potentiometer and light up 0-8 lights
"""

import machine
import neopixel
import time

motd = "2018-12-15 happy"

adc = machine.ADC(0)
np = neopixel.NeoPixel(machine.Pin(4), 8)

while True:
    v = adc.read() #  394 - > 1024
    v = v -394
    v = v / 630
    #  v = v * 8
    l = int(8 * v)

    for i in range(0, l):
        np[i] = (23 ,94 ,11 )
    for i in range(l, 8):
        np[i] = (0, 0, 0)

    np.write()
    print(v)
    time.sleep_ms(250)
