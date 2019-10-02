devices="\
  /strip/command/esp8266_d7524a00 \
  /strip/command/esp8266_51333700 \
  /strip/command/esp8266_8b0e1200 \
  /strip/command/esp8266_a84b4a00 \
  /strip/command/esp8266_88524a00 \
  /strip/command/esp8266_609a1100"

for i in $devices; do
  mosquitto_pub -h 192.168.1.132 -t $i -m $1
  sleep 1
done
