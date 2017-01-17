import RPi.GPIO as GPIO
import time
from random import randint

p = 17

# Length of a dot/dash/etc
ldot = 0.2
ldash = ldot * 3
lspace = ldot * 2
lword = ldot * 6

CODE = {'A': '.-',     'B': '-...',   'C': '-.-.', 
        'D': '-..',    'E': '.',      'F': '..-.',
        'G': '--.',    'H': '....',   'I': '..',
        'J': '.---',   'K': '-.-',    'L': '.-..',
        'M': '--',     'N': '-.',     'O': '---',
        'P': '.--.',   'Q': '--.-',   'R': '.-.',
     	'S': '...',    'T': '-',      'U': '..-',
        'V': '...-',   'W': '.--',    'X': '-..-',
        'Y': '-.--',   'Z': '--..',
        
        '0': '-----',  '1': '.----',  '2': '..---',
        '3': '...--',  '4': '....-',  '5': '.....',
        '6': '-....',  '7': '--...',  '8': '---..',
        '9': '----.',

        ' ': ' ',
        }

def dot():
        print ".",
        GPIO.output(p,GPIO.HIGH)
        time.sleep(ldot)
        GPIO.output(p,GPIO.LOW)
        time.sleep(ldot)
        return

def dash():
        print "-",
        GPIO.output(p,GPIO.HIGH)
        time.sleep(ldash)
        GPIO.output(p,GPIO.LOW)
        time.sleep(ldot)
        return

def space():
        print " ",
        time.sleep(lspace)
        return

def word():
        print "   ",
        time.sleep(lword)
        return

def fade():
    for i in range(100):
        GPIO.output(p,GPIO.HIGH)
        time.sleep(0.0001*i)
        GPIO.output(p,GPIO.LOW)
        time.sleep(0.01)
    for i in range(100,0,-1):
        GPIO.output(p,GPIO.HIGH)
        time.sleep(0.0001*i)
        GPIO.output(p,GPIO.LOW)
        time.sleep(0.01)
    
GPIO.setmode(GPIO.BCM)
GPIO.setup(p, GPIO.OUT)

msg = "SOS SOS SOS SOS SOS "
msg = "314159265358979"
msg = "144"

while True:
   #Message about to transmit
   fade()

   msg = str(randint(0,255))
   for l in msg:
       c = CODE[l.upper()]
       print c,
       for e in c: 
          if e==".": dot()
          if e=="-": dash()
          if e==" ": space()
       space()

   print msg

GPIO.cleanup()
