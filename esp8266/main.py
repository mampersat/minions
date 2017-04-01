import morsecode
import dht, machine
import homeassistant

print("minion v0.1.2")

hass = homeassistant.HomeAssistant('http://jarvis:8123', 'suzymatt')

while True:
    d = dht.DHT22(machine.Pin(5))
    d.measure()
    c = d.temperature()
    f = c * (9.0/5.0) +32
    s = str(f).split('.')[0]
    print(s)
    try:
        new_state = hass.set_state('sensor.temperature', s,
            {'unit_of_measurement': 'F'})
    except:
        print("cant send to homeassistant")

    morsecode.send(s)
