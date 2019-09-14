# Provision
2019-08-29 version

## Prevent needing sudo

```bash
sudo adduser matt dialout
```

## To flash
```bash
/home/matt/.local/bin/esptool.py --port /dev/ttyUSB0 erase_flash

/home/matt/.local/bin/esptool.py --port /dev/ttyUSB0 --baud 460800 write_flash --flash_size=detect 0 ~/Downloads/esp8266-20171101-v1.9.3.bin

picocom /dev/ttyUSB0 -b115200
```

## Connect to network and allow WEBREPL
```python
import network
w = network.WLAN(network.STA_IF)
w.active(True)
w.connect('ShArVa', 'pw-redacted')

w.isconnected()
w.ifconfig()
```

## Enable WebREPL
```python
import webrepl_setup
```