import RPi.GPIO as GPIO
import time
p = 17 

def blink():
        print "High"
        GPIO.output(p,GPIO.HIGH)
        time.sleep(1)
        print "Low"
        GPIO.output(p,GPIO.LOW)
        time.sleep(1)
        return


GPIO.setmode(GPIO.BCM)
GPIO.setup(p, GPIO.OUT)
for i in range(0,50):
        blink()

GPIO.cleanup()
