# pir_module.py


import RPi.GPIO as GPIO
import time
import _thread 
from multiprocessing import Pipe

pir_pin = 40
led_pin = 38

class PIR :

	def __init__(self, pipe) :
		self._armed = None 
		self._motion = False 
		self._looking = False
		self._pipe = pipe
		self.setup()
		
	def setup(self) :
		GPIO.setwarnings(False) 
		GPIO.setmode(GPIO.BOARD) 
		GPIO.setup(pir_pin, GPIO.IN) # Read output from pir motion sensor
		self.disarm()
		self.startWorking()
		
	
	def getState(self) :
		return self._armed, self._motion
		
	def arm(self) :
		self._armed = True 
		#print("PIR sensor ARMED") 		
		
	def disarm(self) :
		self._armed = False 
		#print("PIR sensor DISARMED") 
		
	def startWorking(self) :
		_thread.start_new_thread( self.checking, () )


	def checking(self) :
		while True :
			while self._armed :
				i = GPIO.input(pir_pin)
				if i == 0 :     # When PIR output is low  (No Motion) 
					if self._motion == True :
						self._motion = False
						self._pipe.send(False) 
					else :
						self._motion = False 
					time.sleep(1)
					
				elif i == 1 :
					if self._motion == False :
						self._motion = True
						self._pipe.send(True)
						 
					else :
						self._motion = True 
					time.sleep(1) 


