import RPi.GPIO as GPIO

boardRevision = GPIO.RPI_REVISION
GPIO.setmode(GPIO.BCM)
GPIO.setup(4, GPIO.IN, pull_up_down=GPIO.PUD_UP)

while True:
    read = GPIO.input(4)
    if read:
        print "Vibration!"


