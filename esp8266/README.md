Got a new esp8266? Here's the drill
1. install esptool.py
```
sudo pip install esptool
```
2. Erase the flash
```
sudo /home/matt/.local/bin/esptool.py --port /dev/ttyUSB0 erase_flash
```
3. Download micropython image from http://micropython.org/download#esp8266
4. Write the micropython flash image
```
sudo /home/matt/.local/bin/esptool.py --port /dev/ttyUSB0 --baud 460800 write_flash --flash_size=detect 0 ~/Downloads/esp8266-20171101-v1.9.3.bin
```

5. Connect and confirm `sudo picocom /dev/ttyUSB0 -b115200`
6. `>>>print('Hello world')` dissconnect picocom with ctl-a ctl-x

Connect it to the WiFi
```
sudo picocom /dev/ttyUSB1 -b115200
...
Terminal ready
import network
w = network.WLAN(network.STA_IF)
w.active(True)
w.connect('ShArVa', 'pw-redacted')
w.isconnected()

w.ifconfig()
('192.168.1.137', '255.255.255.0', '192.168.1.1', '192.168.1.1')
```
Probably disconnect the Access point
```
a = network.WLAN(network.AP_IF)
a.active()
a.active(False)
```

Enable WebREPL from picocom USB connection
```
>>>import webrepl_setup
```

Send some files (like main.py) to the device using http://micropython.org/webrepl/ and the IP address

Command line to send files using ampy

```
ampy -p /dev/ttyUSB0 -b 115200 put temp/main.py
```
