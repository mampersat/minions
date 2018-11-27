while :
do
  mosquitto_pub -h 192.168.1.132 -t "strip/command/esp8266_7f35d500" -m 'l8'
  sleep 0.2
  mosquitto_pub -h 192.168.1.132 -t "strip/command/esp8266_7f35d500" -m 'l6'
  sleep 0.2
done
