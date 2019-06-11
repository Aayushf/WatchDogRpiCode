import RPi.GPIO as GPIO
import time
GPIO.cleanup()
GPIO.setmode(GPIO.BCM)
GPIO.setup(16, GPIO.OUT)
while True:
	time.sleep(1)
	GPIO.output(16, GPIO.HIGH)
	time.sleep(1)
	GPIO.output(16, GPIO.LOW)
