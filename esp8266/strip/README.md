sudo /home/matt/.local/bin/esptool.py --port /dev/ttyUSB0 erase_flash
sudo /home/matt/.local/bin/esptool.py --port /dev/ttyUSB0 --baud 460800 write_flash --flash_size=detect 0 ~/Downloads/esp8266-20171101-v1.9.3.bin
sudo picocom /dev/ttyUSB0 -b115200

import network
w = network.WLAN(network.STA_IF)
w.active(True)
w.connect('ShArVa', 'end dirt people main zero')
w.isconnected()

import webrepl_setup

ampy -p /dev/ttyUSB0 -b 115200 put main.py; sudo picocom /dev/ttyUSB0 -b115200
