while :
do
  mosquitto_pub -h 192.168.1.132 -t "strip/command/esp8266_7f35d500" -m 'l8'
  sleep 0.2
  mosquitto_pub -h 192.168.1.132 -t "strip/command/esp8266_7f35d500" -m 'l6'
  sleep 0.2
  mosquitto_pub -h 192.168.1.132 -t "strip/command/esp8266_7f35d500" -m 'l5'
  sleep 0.2
  mosquitto_pub -h 192.168.1.132 -t "strip/command/esp8266_7f35d500" -m 'l4'
  sleep 0.2
  mosquitto_pub -h 192.168.1.132 -t "strip/command/esp8266_7f35d500" -m 'l3'
  sleep 0.2
  mosquitto_pub -h 192.168.1.132 -t "strip/command/esp8266_7f35d500" -m 'l2'
  sleep 0.2
  mosquitto_pub -h 192.168.1.132 -t "strip/command/esp8266_7f35d500" -m 'l1'
  sleep 0.2
done
