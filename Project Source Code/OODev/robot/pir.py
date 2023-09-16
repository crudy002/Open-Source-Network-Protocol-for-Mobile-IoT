import RPi.GPIO as GPIO
import time 
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(21, GPIO.IN)	# Read output from pir motion sensor
GPIO.setup(20, GPIO.OUT) 
GPIO.output(20, 0) 


try:	
	while True :
		i = GPIO.input(21)
		if i == 0 :	# When PIR output is low  (No Motion) 
			print("No Motion...") 
			GPIO.output(20, 0)  
			time.sleep(.5)
		elif i == 1 :
			print("Intrusion Detected, STOP IT!") 
			GPIO.output(20, 1) 
			time.sleep(.5)
except KeyboardInterrupt :
	GPIO.cleanup()
