mosquitto_pub -h 192.168.1.132 -t "leds/esp8266_8f141200" -m 'l8'
mosquitto_pub -h 192.168.1.132 -t "leds/esp8266_8b0e1200" -m 'l8'
mosquitto_pub -h 192.168.1.132 -t "leds/esp8266_5133d500" -m 'l8'
mosquitto_pub -h 192.168.1.132 -t "leds/esp8266_51333700" -m 'l8'
sleep 2

mosquitto_pub -h 192.168.1.132 -t "leds/esp8266_8f141200" -m 'l6'
mosquitto_pub -h 192.168.1.132 -t "leds/esp8266_8b0e1200" -m 'l6'
mosquitto_pub -h 192.168.1.132 -t "leds/esp8266_5133d500" -m 'l6'
mosquitto_pub -h 192.168.1.132 -t "leds/esp8266_51333700" -m 'l6'
sleep 1

mosquitto_pub -h 192.168.1.132 -t "leds/esp8266_8f141200" -m 'l7'
mosquitto_pub -h 192.168.1.132 -t "leds/esp8266_8b0e1200" -m 'l7'
mosquitto_pub -h 192.168.1.132 -t "leds/esp8266_5133d500" -m 'l7'
mosquitto_pub -h 192.168.1.132 -t "leds/esp8266_51333700" -m 'l7'
sleep 1

mosquitto_pub -h 192.168.1.132 -t "leds/esp8266_8f141200" -m 'l5'
mosquitto_pub -h 192.168.1.132 -t "leds/esp8266_8b0e1200" -m 'l5'
mosquitto_pub -h 192.168.1.132 -t "leds/esp8266_5133d500" -m 'l5'
mosquitto_pub -h 192.168.1.132 -t "leds/esp8266_51333700" -m 'l5'
sleep 1


mosquitto_pub -h 192.168.1.132 -t "leds/esp8266_8f141200" -m 'l3'
mosquitto_pub -h 192.168.1.132 -t "leds/esp8266_8b0e1200" -m 'l3'
mosquitto_pub -h 192.168.1.132 -t "leds/esp8266_5133d500" -m 'l3'
mosquitto_pub -h 192.168.1.132 -t "leds/esp8266_51333700" -m 'l3'
sleep 0.5

mosquitto_pub -h 192.168.1.132 -t "leds/esp8266_8f141200" -m 'l0'
mosquitto_pub -h 192.168.1.132 -t "leds/esp8266_8b0e1200" -m 'l0'
mosquitto_pub -h 192.168.1.132 -t "leds/esp8266_5133d500" -m 'l0'
mosquitto_pub -h 192.168.1.132 -t "leds/esp8266_51333700" -m 'l0'
sleep 1.5


mosquitto_pub -h 192.168.1.132 -t "leds/esp8266_8f141200" -m 'l9'
mosquitto_pub -h 192.168.1.132 -t "leds/esp8266_8b0e1200" -m 'l9'
mosquitto_pub -h 192.168.1.132 -t "leds/esp8266_5133d500" -m 'l9'
mosquitto_pub -h 192.168.1.132 -t "leds/esp8266_51333700" -m 'l9'
sleep 4
