devices="\
  /strip/command/esp8266_8f141200 \
  /strip/command/esp8266_8b0e1200 \
  /strip/command/esp8266_5133d500 \
  /strip/command/esp8266_51333700 \
  /strip/command/esp8266_609a1100 \
  /strip/command/esp8266_7f35d500 \
  /strip/command/esp8266_c1584a00"

for i in $devices; do
  mosquitto_pub -h 192.168.1.132 -t $i -m $1
done
