from machine import I2C, Pin
import time
import morsecode

i2c = I2C(freq=400000, scl=Pin(5), sda = Pin(4))

# activate accelerometer
i2c.writeto_mem(29, 0x2a, b'\x01')

x = y = z = 0

while True:
  r = i2c.readfrom_mem(29,0x01,6)

  # Calculate diff
  xd = x - r[0]
  yd = y - r[2]
  zd = z - r[4]

  # Remember readings
  x = r[0]
  y = r[2]
  z = r[4]

  total = abs(xd) + abs(yd) + abs(zd)

  if (total >5):
      vibration = "XXX"
      morsecode.send("A")
  else:
      vibration = ""

  print(total, vibration)

# for i in range(0, 3):
#    print(r[i], end="\t")

  time.sleep(0.1)
