# 192.168.1.119 , esp8266_609a1100, test board
# 192.168.1.116 , , window, D
# 192.168.1.111 , esp8266_22584a00, long strip, C
# 192.168.1.118 , esp8266_8b0e1200, master east, E

report:
	export AMPY_PORT=/dev/ttyUSB0
	ampy run report.py

test:
	ampy run main.py

192.168.1.119:
	../webrepl/webrepl_cli.py -p $$SECRET main.py 192.168.1.119:main.py
	../webrepl/webrepl_cli.py -p $$SECRET char/192.168.1.119.py 192.168.1.119:config.py

192.168.1.111:
	../webrepl/webrepl_cli.py -p $$SECRET main.py 192.168.1.111:main.py
	../webrepl/webrepl_cli.py -p $$SECRET char/192.168.1.111.py 192.168.1.111:config.py

192.168.1.116:
	../webrepl/webrepl_cli.py -p $$SECRET main.py 192.168.1.116:main.py
	../webrepl/webrepl_cli.py -p $$SECRET char/192.168.1.116.py 192.168.1.116:config.py

192.168.1.118:
	../webrepl/webrepl_cli.py -p $$SECRET main.py 192.168.1.118:main.py
	../webrepl/webrepl_cli.py -p $$SECRET char/192.168.1.118.py 192.168.1.118:config.py

publish: 192.168.1.119 192.168.1.111 192.168.1.116