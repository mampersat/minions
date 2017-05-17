import morsecode
import dht, machine
import homeassistant

print("minion v0.1.2")

sensor_name = 'sensor.minion5'
hass = homeassistant.HomeAssistant('http://jarvis:8123', 'suzymatt')

adc = machine.ADC(0)

while True:
    l = adc.read()
    print("lux",l)
    try:
        new_state = hass.set_state('sensor.sunroom_lux', str(l),
            {'unit_of_measurement': 'L',
             'friendly_name': 'sensor.sunroom_lux'})
    except Exception as inst:
        print('cant send to homeassistant')
        print(inst)

    d = dht.DHT22(machine.Pin(5))
    d.measure()
    c = d.temperature()
    f = c * (9.0/5.0) +32
    s = str(f).split('.')[0]
    print("temp",s)
    try:
        new_state = hass.set_state('sensor.sunroom_temp', s,
            {'unit_of_measurement': 'F',
             'friendly_name':'sensor.sunroom_temp'})
    except:
        print("cant send to homeassistant")

    morsecode.send(s)
