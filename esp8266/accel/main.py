""" Furnace vibration minion

Measure accelerometer movement and log time the furnace is on

Accelerometer = https://learn.adafruit.com/adafruit-mma8451-accelerometer-breakout/overview

"""

import machine
import time
import ubinascii
import webrepl

from umqtt.simple import MQTTClient

import homeassistant
import morsecode

print("Running v0.2")

# Fucked around with a 20 SENSITIVITY prev
SENSITIVITY = 5
LOOP_SLEEP = 0.1

# MQTT settings
topic = 'home'
discovery_prefix = 'homeassistant'
heartbeat_component = 'binary_sensor'
time_component = 'sensor'
node_id = 'furnace'
heartbeat_object_id = 'heartbeat'
time_object_id = 'time'
broker = 'jarvis'
client_id = 'esp8266_'+str(ubinascii.hexlify(machine.unique_id()), 'utf-8')
client = MQTTClient(client_id, broker)

# building in fault tolerance - it's OK to keep running w/o a connection
# client.connect()

heartbeat = 1

# Register with HomeAssistant
#client.publish("homeassistant/sensor/sensorFurnaceHB/config",
#               '{"device_class":"sensor","name": "Heartbeat", "state_topic":"/homeassistant/sensor/sensorFurnaceHB/state" }')

#client.publish("homeassistant/sensor/sensorFurnaceT/config",
#               '{"device_class":"sensor","name": "Vibration", "state_topic":"/homeassistant/sensor/sensorFurnaceT/state" }')

# create i2c object to talk to accelerometer
i2c = machine.I2C(freq=400000, scl=machine.Pin(5), sda=machine.Pin(4))

# activate accelerometer
i2c.writeto_mem(29, 0x2a, b'\x01')

# are we currently vibrating
recording = False
start = time.time()

led = machine.Pin(2, machine.Pin.OUT)


def listen_for_a_sec():
    """Ping 10 times in a second for motion, return true if detected
    """
    ret = False
    x = y = z = 0
    for t in range(0, 10):

        # read registers from accelerometer
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

        # are we vibrating?
        if (total > SENSITIVITY) and (t > 0):
            ret = True

        time.sleep(LOOP_SLEEP)

    return ret

def frangable_publish(topic, payload):
    """If power goes out - we may try to log before homeassistant is back
    so if we fail - sleep a bit and try to reconnect the mqtt client
    drop current message on the floor
    """
    try:
        client.publish(topic, payload)
    except:
        print("failed to log, sleeping 10")
        time.sleep(10)
        try:
            client.connect()
        except:
            print("failed to connect")


while True:

    # send heartbeat

    frangable_publish("homeassistant/sensor/sensorFurnaceHB/state", str(heartbeat))
    heartbeat = - heartbeat

    if listen_for_a_sec():
        led.low()  # on
        frangable_publish("homeassistant/sensor/sensorFurnaceBurn/state", "1")
        if not recording:
            print("start")
            start = time.time()
            recording = True
    else:
        led.high()  # off
        frangable_publish("homeassistant/sensor/sensorFurnaceBurn/state", "0")
        if recording:
            print("end")
            timespan = time.time() - start
            print(timespan)
            data = str(timespan)
            frangable_publish("homeassistant/sensor/sensorFurnaceT/state", bytes(str(data), 'utf-8'))

        recording = False
