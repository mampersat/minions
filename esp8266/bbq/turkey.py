import paho.mqtt.client as mqtt


def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("/bbq/esp8266_7f35d500")


def on_message(client, userdata, msg):
    print(msg.topic+" ? "+str(msg.payload))
    t = msg.payload.split('.')[0]
    i = int(t)
    s = str(i)
    a = 'l' + s[0]
    b = 'l' + s[1]
    c = 'l' + s[2]
    mqttc.publish("leds/esp8266_5133d500", a)
    mqttc.publish("leds/esp8266_8f141200", b)
    mqttc.publish("leds/esp8266_8b0e1200", c)



client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("192.168.1.132")

client.loop_forever()
