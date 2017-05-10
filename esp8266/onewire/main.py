"""Read onewire sensors and report to HomeAssistant"""
import network
import morsecode
import homeassistant
from machine import Pin
import onewire
import time, ds18x20

print("minion v0.1.8")

names = {'ow28ff51d0c11604ce':'master_bedroom_temp',
    'ow28ff3734c21604e0':'outside_north',
    'ow28ff9307c11604e8':'hallway',
}

w = network.WLAN(network.STA_IF)
# give the device a second to get connected
time.sleep(1)
print(w.ifconfig())

hass = homeassistant.HomeAssistant('http://jarvis:8123', 'suzymatt')

ow = onewire.OneWire(Pin(12))
ds = ds18x20.DS18X20(ow)
roms = ds.scan()

while True:

    print(w.ifconfig()) # Inside loop as network takes a few cycles to connect

    ds.convert_temp()
    time.sleep_ms(750)

    i=0
    for rom in roms:

        # construct sensor name containing onewire device address
        addr = 'ow' + ''.join('{:02x}'.format(x) for x in rom)
        if addr in names:
            s = 'sensor.' + names[addr]
        else:
            s = 'sensor.' + addr

        c = ds.read_temp(rom)
        f = c * (9.0/5.0) +32

        print(s,':',f)

        try:
            new_state = hass.set_state(s, str(f),
                {'unit_of_measurement': 'F'})
                 # 'friendly_name': s})
            print("# Logged")
        except Exception as inst:
            print('cant send to homeassistant')
            print(inst)

        # blink integer temp value
        m = str(f).split('.')[0]
        morsecode.send(m)
        i += 1
