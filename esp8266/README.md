Got a new esp8266? Here's the drill
1. install esptool.py `sudo pip install esptool`
2. Erase the flash `sudo /home/matt/.local/bin/esptool.py --port /dev/ttyUSB1 erase_flash`
3. Download micropython image from http://micropython.org/download#esp8266
4. Write the micropython flash image `sudo /home/matt/.local/bin/esptool.py --port /dev/ttyUSB1 --baud 460800 write_flash --flash_size=detect 0 ~/Downloads/esp8266-20170108-v1.8.7.bin`
5. Connect and confirm `sudo picocom /dev/ttyUSB1 -b115200`
6. `>>>print('Hello world')` dissconnect picocom with ctl-a ctl-c

Connect it to the WiFi
```
sudo picocom /dev/ttyUSB1 -b115200
...
Terminal ready
>>> import network
>>> sta_if = network.WLAN(network.STA_IF)
>>> sta_if.active(True)
#6 ets_task(4020ed88, 28, 3fff9fa8, 10)
>>> sta_if.connect('ShArVa')
>>> sta_if.isconnected()
True
>>> sta_if.ifconfig()
('192.168.1.137', '255.255.255.0', '192.168.1.1', '192.168.1.1')
```

Enable WebREPL from picocom USB connection
```
>>>import webrepl_setup
```

Send some files (like main.py) to the device using http://micropython.org/webrepl/ and the IP address