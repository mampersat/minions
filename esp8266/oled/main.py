"""Read onewire sensors and report to HomeAssistant"""
import network
import morsecode
import homeassistant
from machine import Pin
import onewire
import time, ds18x20
import ssd1306, machine

print("minion v0.1.8")

def calc_y(y):
    return 64 - int(y-60)

# Setup OLED
i2c = machine.I2C(freq=400000,scl=machine.Pin(5),sda=machine.Pin(4))
oled = ssd1306.SSD1306_I2C(128,64,i2c)
g= []
outside="nil"

# Dicstionary mapping one-wire ID to friendly name
names = {'ow28ff51d0c11604ce':'master_bedroom_temp',
    'ow28ff3734c21604e0':'outside_north',
    'ow28ff9307c11604e8':'hallway',
    'ow28ff283cb51603f9':'minion7',
}

w = network.WLAN(network.STA_IF)
# give the device a second to get connected
time.sleep(1)
print(w.ifconfig())

# Setup homeassistant API endpoint
hass = homeassistant.HomeAssistant('http://jarvis:8123', 'suzymatt')

# Setup onewire probing
ow = onewire.OneWire(Pin(12))
ds = ds18x20.DS18X20(ow)
roms = ds.scan()

# Setup reed switch
reed = machine.Pin(13, machine.Pin.IN, machine.Pin.PULL_UP)

i = 0
remove = 1.0

while True:

    print(w.ifconfig()) # Inside loop as network takes a few cycles to connect

    ds.convert_temp()
    # time.sleep_ms(250)

    for rom in roms:

        # construct sensor name containing onewire device address
        addr = 'ow' + ''.join('{:02x}'.format(x) for x in rom)
        if addr in names:
            s = 'sensor.' + names[addr]
        else:
            s = 'sensor.' + addr

        c = ds.read_temp(rom)
        f = c * (9.0/5.0) +32

        #debug
        #print(s,':',f)

        # write to homeassistant
        if (i%100) == 0:
            try:
                # new_state = hass.set_state(s, str(f),
                #     {'unit_of_measurement': 'F'})
                print("# Logged")

                outside = hass.get_state("sensor.outside_north")['state']
            except Exception as inst:
                print('cant send to homeassistant')
                print(inst)

    m = str(f).split('.')[0]

    oled.fill(0)
    oled.text("Inside : " + str(f),0,0)
    oled.text("Outside: " + outside,0,9)

    # graphing
    g.append(f)
    if len(g) > 128:
        g.pop(129-int(remove))
        remove = remove * 2
        print(remove , "removed")
        if remove >128:
            remove = 1.0

    x = 0
    for y in g:
        x += 1
        oled.pixel(x,calc_y(y),1)
        if ((x+i)%10) ==0:
            oled.pixel(x,calc_y(70),1)
            oled.pixel(x,63,1)

    # check reed switch
    reed_s = "unknown"
    if reed.value():
        reed_s = "closed"
    else:
        reed_s = "open"

    oled.text(reed_s, 21, 18)

    oled.show()
    i += 1
