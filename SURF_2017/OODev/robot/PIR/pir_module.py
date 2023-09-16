# pir_module.py


import RPi.GPIO as GPIO
import time
import _thread 

pir_pin = 40
led_pin = 38

class PIR :

	def __init__(self) :
		self._armed = None 
		self._motion = False 
		self._looking = False
		self.setup()
		
	def setup(self) :
		GPIO.setwarnings(False) 
		GPIO.setmode(GPIO.BOARD) 
		GPIO.setup(pir_pin, GPIO.IN) # Read output from pir motion sensor
		#GPIO.setup(led_pin, GPIO.OUT)
		#GPIO.output(led_pin, 0)
		self.disarm()
		self.startWorking()
		
	
	def getState(self) :
		return self._armed, self._motion
		
	def arm(self) :
		self._armed = True 
		
	def disarm(self) :
		self._armed = False 
		
	def startWorking(self) :
		_thread.start_new_thread( self.checking, () )


	def checking(self) :
		while True :
			while self._armed :
				i = GPIO.input(pir_pin)
				if i == 0 :     # When PIR output is low  (No Motion) 
					print("No Motion...")
					self._motion = False
					#GPIO.output(led_pin, 0)
					time.sleep(2)
				elif i == 1 :
					print("Intrusion Detected, STOP IT!")
					self._motion = True
					#GPIO.output(led_pin, 1)
					time.sleep(2)
			print("Not armed") 	


