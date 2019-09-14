# output device specific info
import machine
import network
import time
import ubinascii

print("Reporting...")

client_id = 'esp8266_'+str(ubinascii.hexlify(machine.unique_id()), 'utf-8')

s = network.WLAN(network.STA_IF)
while not s.isconnected():
    print("Network not connected - sleeping")
    time.sleep(1)

ip = s.ifconfig()[0]

print(ip, ",", client_id)