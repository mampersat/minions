import network
import morsecode
import homeassistant
from machine import Pin
import onewire
import time, ds18x20

print("minion v0.1.5")

w = network.WLAN(network.STA_IF)
print(w.ifconfig())


hass = homeassistant.HomeAssistant('http://jarvis:8123', 'suzymatt')

ow = onewire.OneWire(Pin(12))
ds = ds18x20.DS18X20(ow)
roms = ds.scan()

while True:
    print(w.ifconfig())

    ds.convert_temp()
    time.sleep_ms(750)

    for rom in roms:

        s = 'sensor.ow-' + ''.join('{:02x}'.format(x) for x in rom)

        c = ds.read_temp(rom)
        f = c * (9.0/5.0) +32

        print(s,':',f)

        try:
            new_state = hass.set_state('sensor.test', str(f),
                {'unit_of_measurement': 'F',
                 'friendly_name': 'sensor.test'})
        except Exception as inst:
            print('cant send to homeassistant')
            print(inst)

        s = str(f).split('.')[0]
        morsecode.send(s)
