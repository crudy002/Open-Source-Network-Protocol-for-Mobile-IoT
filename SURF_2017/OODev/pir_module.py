# pir_module.py


import RPi.GPIO as GPIO
import time
import thread 


class PIR :

	def __init__(self) :
		self._armed = None 
		self._motion = False 
		self.setup()
		
	def setup(self) :
		GPIO.setup(21, GPIO.IN) # Read output from pir motion sensor
		GPIO.setup(20, GPIO.OUT)
		GPIO.output(20, 0)
		self.disarm()
		self.startWorking()
		
	
	def getState(self) :
		return self._armed, self._motion
		
	def arm(self) :
		self._armed = True 
		
	def disarm(self) :
		self._armed = False 
		
	def startWorking(self) :
		thread.start_new_thread( self.checking() ) 
		
	
	def checking(self) :
		while True :
			while self._armed :
				i = GPIO.input(21)
				if i == 0 :     # When PIR output is low  (No Motion) 
					print("No Motion...")
					self._motion = False
					GPIO.output(20, 0)
					time.sleep(.5)
				elif i == 1 :
					print("Intrusion Detected, STOP IT!")
					self._motion = True
					GPIO.output(20, 1)
					time.sleep(.5)
        



