../webrepl/webrepl_cli.py -p $SECRET ~/git/minions/esp8266/strip/main.py 192.168.1.149:
mosquitto_pub -h 192.168.1.132 -t "strip/command/esp8266_7f35d500" -m 'b'
