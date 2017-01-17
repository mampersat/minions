import RPi.GPIO as GPIO
import time
p = 17

# Length of a dot/dash/etc
dot = 0.5
dash = dot * 3
space = dot * 2
word = dot * 6

def dot():
        print "."
        GPIO.output(p,GPIO.HIGH)
        time.sleep(dot)
        GPIO.output(p,GPIO.LOW)
        time.sleep(dot)
        return

def dash():
        print "-"
        GPIO.output(p,GPIO.HIGH)
        time.sleep(dash)
        GPIO.output(p,GPIO.LOW)
        time.sleep(dot)
        return

def space():
        print " "
        time.sleep(space)
        return

def word():
        print "   "
        time.sleep(word)
        return

GPIO.setmode(GPIO.BCM)
GPIO.setup(p, GPIO.OUT)
for i in range(0,50):
        dot()
        dot()
        dot()
        dash()
        dash()
        dash()
        dot()
        dot()
        dot()
        space()

GPIO.cleanup()
