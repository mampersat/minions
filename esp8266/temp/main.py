""" Furnace vibration minion

Measure accelerometer movement and log time the furnace is on
"""

import ds18x20
import machine
import onewire
import time
import ubinascii
import webrepl

from umqtt.simple import MQTTClient

import homeassistant
import morsecode

print("Running temp/main v0.5")

# MQTT settings
topic = 'home'
broker = 'jarvis'
client_id = 'esp8266_'+str(ubinascii.hexlify(machine.unique_id()), 'utf-8')
print("client_id = "+client_id)
client = MQTTClient(client_id, broker)

names = {'ow28ff51d0c11604ce':'mobile_temp',
    'ow28ff3734c21604e0':'outside_north',
    'ow28ff9307c11604e8':'hallway',
}

# building in fault tolerance - it's OK to keep running w/o a connection
# client.connect()

led = machine.Pin(2, machine.Pin.OUT)

def frangable_publish(topic, payload):
    """If power goes out - we may try to log before homeassistant is back
    so if we fail - sleep a bit and try to reconnect the mqtt client
    drop current message on the floor
    """
    try:
        client.publish(topic, payload)
        print("Wrote", payload)
    except:
        print("failed to log, sleeping 10")
        time.sleep(10)
        try:
            client.connect()
        except:
            print("failed to connect")

ow = onewire.OneWire(machine.Pin(12))
ds = ds18x20.DS18X20(ow)
roms = ds.scan()

# sleep to allow wifi to connect
time.sleep(1)

while True:

    ds.convert_temp()

    i=0
    for rom in roms:

        # construct sensor name containing onewire device address
        addr = 'ow' + ''.join('{:02x}'.format(x) for x in rom)
        if addr in names:
            s = names[addr]
        else:
            s = addr

        c = ds.read_temp(rom)
        f = c * (9.0/5.0) +32

        t = "homeassistant/sensor/" + s + "/state"
        p = bytes(str(f), 'utf-8')

        frangable_publish(t, p)

        time.sleep(5)
