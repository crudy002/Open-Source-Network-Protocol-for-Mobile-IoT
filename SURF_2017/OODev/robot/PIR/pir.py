import RPi.GPIO as GPIO
import time 
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(40, GPIO.IN)	# Read output from pir motion sensor
GPIO.setup(38, GPIO.OUT) 
GPIO.output(38, 0) 


try:	
	while True :
		i = GPIO.input(40)
		if i == 0 :	# When PIR output is low  (No Motion) 
			print("No Motion...") 
			GPIO.output(38, 0)  
			time.sleep(.5)
		elif i == 1 :
			print("Intrusion Detected, STOP IT!") 
			GPIO.output(38, 1) 
			time.sleep(.5)
except KeyboardInterrupt :
	GPIO.cleanup()
