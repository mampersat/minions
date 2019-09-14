# Requirements
For code running on the ESP8266

- Frangibility
  - [ ] recover from power outage w/o Wifi or MQTT

- Ability to be inventoried
  - [ ] Connectivity from central system
  - [ ] Wake up should register and/or get latest info

- Updateable over the air
  - [ ] Code can be pushed and device will restart

- Heartbeat : MQTT reporting and visual
  -[ ] Similar to inventory but scheduled (Like CRON H function)

- Small codebase: Leave room for patterns
  - [ ] Code coverage via testing, delete what is not used
  - [ ] Maybe a compiliation step that squashes 

- Patterns
  - [ ] Diagnostic : test_segments does the binary thing now

## Startup Cycle
Do we want a startup cycle, or do we want to go straight to visual indication of operation


## Inventory
- A : 192.168.1.117
- B : 192.168.1.119
- C : 192.168.1.111
- D : 192.168.1.149
-   : 192.168.1.116 Desk Window

/strip/health/esp8266_51333700 09-01:2:alive 09-01:2 192.168.1.116

## Burn test
Time: 2019-09-01 11:07:19.883037 : Started full bright test 1.5

/strip/health/esp8266_22584a00 09-01:1:test 1.3

Full bright kills it quick
Test increasing brightness
206 : Freeze
217 : Reset

Calculation from https://learn.adafruit.com/adafruit-neopixel-uberguide/powering-neopixels details needed 3A

Testing 50 pixels @ 255: Ran for 10+min

