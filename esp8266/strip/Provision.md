# Provision new ESP8266

## Flash micropython to device
```bash
/home/matt/.local/bin/esptool.py --port /dev/ttyUSB0 erase_flash
esptool.py --port /dev/ttyUSB0 --baud 460800 write_flash --flash_size=detect 0 ~/Downloads/esp8266-20180511-v1.9.4.bin
picocom /dev/ttyUSB0 -b115200
```

## Connect to network
```python
import network
w = network.WLAN(network.STA_IF)
w.active(True)
w.connect('ShArVa', 'pw-redacted')
```

### Fix password before continue
``` python
w.isconnected()

import webrepl_setup
```

## Send main.py to device
```bash
ampy -p /dev/ttyUSB0 -b 115200 put main.py
```
