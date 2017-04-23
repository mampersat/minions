Got a new esp8266? Here's the drill
1. install esptool.py `sudo pip install esptool`
2. Erase the flash `sudo /home/matt/.local/bin/esptool.py --port /dev/ttyUSB1 erase_flash`
3. Download micropython image from http://micropython.org/download#esp8266
4. Write the micropython flash image `sudo /home/matt/.local/bin/esptool.py --port /dev/ttyUSB1 --baud 460800 write_flash --flash_size=detect 0 ~/Downloads/esp8266-20170108-v1.8.7.bin`
5. Connect and confirm `sudo picocom /dev/ttyUSB1 -b115200`
6. `>>>print('Hello world')` dissconnect picocom with <ctl>-a <ctl>-c
