# Read analog pin

import machine
import network
import socket
import time

s = network.WLAN(network.STA_IF)
while not s.isconnected():
    print("Network not connected - sleeping")
    time.sleep(1)

SERVER = '192.168.1.129'
PORT = 2003
sock = socket.socket()
sock.connect( ( SERVER, PORT))

adc = machine.ADC(0)

while True:

    v = adc.read()
    t = -1
    message = 'plant.moisture.fern %d %d\n' % (v, t )
    sock.sendall(message)
    print(message)
    time.sleep(1)
