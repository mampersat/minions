# 192.168.1.119 , esp8266_609a1100, test board, B
# 192.168.1.116 , , window, D
# 192.168.1.111 , esp8266_22584a00, long strip, C
# 192.168.1.118 , esp8266_8b0e1200, master west, E
# 192.168.1.101 , esp8266_a84b4a00, master east, G
# 192.168.1.145 , esp8266_d7524a00, , H

# DEAD
# 192.168.1.101 ,  esp8266_09971100 , master east, F

test:
	ampy run main.py

report:
	ampy run report.py

192.168.1.119:
	-../webrepl/webrepl_cli.py -p $$SECRET main.py 192.168.1.119:main.py
	# ../webrepl/webrepl_cli.py -p $$SECRET char/192.168.1.119.py 192.168.1.119:config.py

192.168.1.111:
	-../webrepl/webrepl_cli.py -p $$SECRET main.py 192.168.1.111:main.py
	# ../webrepl/webrepl_cli.py -p $$SECRET char/192.168.1.111.py 192.168.1.111:config.py

192.168.1.116:
	-../webrepl/webrepl_cli.py -p $$SECRET main.py 192.168.1.116:main.py
	# ../webrepl/webrepl_cli.py -p $$SECRET char/192.168.1.116.py 192.168.1.116:config.py

192.168.1.118:
	-../webrepl/webrepl_cli.py -p $$SECRET main.py 192.168.1.118:main.py
	# ../webrepl/webrepl_cli.py -p $$SECRET char/192.168.1.118.py 192.168.1.118:config.py

192.168.1.101:
	-../webrepl/webrepl_cli.py -p $$SECRET main.py 192.168.1.101:main.py
	# ../webrepl/webrepl_cli.py -p $$SECRET char/192.168.1.101.py 192.168.1.101:config.py

192.168.1.145:
	-../webrepl/webrepl_cli.py -p $$SECRET main.py 192.168.1.145:main.py
	# ../webrepl/webrepl_cli.py -p $$SECRET char/192.168.1.145.py 192.168.1.145:config.py

publish: 192.168.1.119 192.168.1.111 192.168.1.116 192.168.1.118 192.168.1.101