import RPi.GPIO as GPIO

pin = 9
boardRevision = GPIO.RPI_REVISION
GPIO.setmode(GPIO.BCM)
GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

while True:
    read = GPIO.input(pin)
    print read,

