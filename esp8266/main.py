import morsecode
import dht, machine
import homeassistant

print("minion v0.1.2")

hass = homeassistant.HomeAssistant('http://jarvis:8123', 'suzymatt')

adc = machine.ADC(0)

while True:
    l = adc.read()
    print("lux",l)
    try:
        new_state = hass.set_state('sensor.minion3_lux', str(l),
            {'unit_of_measurement': 'L',
             'friendly_name': 'esp1 lux'})
    except:
        print('cant send to homeassistant')

    d = dht.DHT22(machine.Pin(5))
    d.measure()
    c = d.temperature()
    f = c * (9.0/5.0) +32
    s = str(f).split('.')[0]
    print("temp",s)
    try:
        new_state = hass.set_state('sensor.minion3_temp', s,
            {'unit_of_measurement': 'F',
             'friendly_name':'esp1 temp'})
    except:
        print("cant send to homeassistant")

    morsecode.send(s)
