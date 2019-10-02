# B , 0 , 192.168.1.119 , esp8266_609a1100
# H , 1 , 192.168.1.146 , esp8266_d7524a00
# D , 2 , 192.168.1.116 , esp8266_51333700 
# G , 4 , 192.168.1.101 , esp8266_a84b4a00
# K , 5 , 192.168.1.122 , esp8266_88524a00
# E = 6 # 192.168.1.118 , esp8266_8b0e1200

# 192.168.1.122 , esp8266_22584a00, long strip, C
# 192.168.1.133 , esp8266_09971100 , , J
# 192.168.1.121 , esp8266_ee534a00, 
# esp8266_d7524a00
# DEAD
# 192.168.1.101 ,  esp8266_09971100 , master east, F
# 192.168.1.119 , esp8266_609a1100, test board, B

report:
	ampy run report.py

flash:
	esptool.py --port /dev/ttyUSB0 erase_flash
	esptool.py --port /dev/ttyUSB0 --baud 460800 write_flash --flash_size=detect 0 ~/Downloads/esp8266-20190529-v1.11.bin
	picocom /dev/ttyUSB0 -b115200

test:
	ampy -p /dev/ttyUSB0 -b 115200 put main.py; sudo picocom /dev/ttyUSB0 -b115200

192.168.1.146:
	-../webrepl/webrepl_cli.py -p $$SECRET main.py 192.168.1.146:main.py
	sleep 1
	-../webrepl/webrepl_cli.py -p $$SECRET char/192.168.1.146.py 192.168.1.146:config.py

192.168.1.118:
	-../webrepl/webrepl_cli.py -p $$SECRET main.py 192.168.1.118:main.py
	sleep 1
	-../webrepl/webrepl_cli.py -p $$SECRET char/192.168.1.118.py 192.168.1.118:config.py

192.168.1.101:
	-../webrepl/webrepl_cli.py -p $$SECRET main.py 192.168.1.101:main.py
	sleep 1
	-../webrepl/webrepl_cli.py -p $$SECRET char/192.168.1.101.py 192.168.1.101:config.py

192.168.1.122:
	-../webrepl/webrepl_cli.py -p $$SECRET main.py 192.168.1.122:main.py
	sleep 1
	-../webrepl/webrepl_cli.py -p $$SECRET char/192.168.1.122.py 192.168.1.122:config.py

192.168.1.116:
	-../webrepl/webrepl_cli.py -p $$SECRET main.py 192.168.1.116:main.py
	sleep 1
	-../webrepl/webrepl_cli.py -p $$SECRET char/192.168.1.116.py 192.168.1.116:config.py

192.168.1.119:
	-../webrepl/webrepl_cli.py -p $$SECRET main.py 192.168.1.119:main.py
	sleep 1
	-../webrepl/webrepl_cli.py -p $$SECRET char/192.168.1.119.py 192.168.1.119:config.py

publish: 192.168.1.146 192.168.1.118 192.168.1.101 192.168.1.122 192.168.1.116 192.168.1.119

