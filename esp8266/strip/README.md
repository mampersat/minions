# xmas lights
> esp8266 controlled xmas lights

<img src="top4windows.jpg">

## Technologies used
* [esp8266](https://www.esp8266.com/wiki/doku.php?id=getting-started-with-the-esp8266)
* [ws2812b LED strips](https://www.google.com/search?q=ws2812b&source=univ&tbm=shop&tbo=u&sa=X&ved=0ahUKEwi5883CsfLeAhWjxVkKHTRFBToQsxgILQ&biw=1333&bih=1221)
* [micropython](https://micropython.org/)
* [mqtt](http://mqtt.org/)

A seven segment prototype hooked to the esp8266
<img src="prototype.jpg">

Using 10baseT wire to connect indoor esp8266 to outdoor 2s2821b
<img src="wireLEDend.jpg">

Flash esp8266 with micropython
```
sudo /home/matt/.local/bin/esptool.py --port /dev/ttyUSB0 erase_flash
sudo /home/matt/.local/bin/esptool.py --port /dev/ttyUSB0 --baud 460800 write_flash --flash_size=detect 0 ~/Downloads/esp8266-20171101-v1.9.3.bin
sudo picocom /dev/ttyUSB0 -b115200
```

Connect the esp8266 to the wifi
```
import network
w = network.WLAN(network.STA_IF)
w.active(True)
w.connect('ShArVa', 'pw-redacted')
w.isconnected()
```

Enable wifi based webrepl to upload new code
```
import webrepl_setup
```

Push new code over USB connection
```
ampy -p /dev/ttyUSB0 -b 115200 put main.py; sudo picocom /dev/ttyUSB0 -b115200
```
