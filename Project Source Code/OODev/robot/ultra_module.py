# ultra_module.py

import RPi.GPIO as GPIO
import time
import _thread 

TRIG = 35
ECHO = 36

class ULTRA :

	def __init__(self) :
		self._distance = 0 
		self.setup() 
		
	def getDistance(self) :
		return self._distance

	def setup(self) :

		GPIO.setmode(GPIO.BOARD) 
		GPIO.setwarnings(False) 
		GPIO.setup(TRIG, GPIO.OUT) 
		GPIO.setup(ECHO, GPIO.IN)
		self.startWorking() 

	def distance(self) :
		GPIO.output(TRIG, 0) 
		time.sleep(0.000002) 
		GPIO.output(TRIG, 1) 
		time.sleep(0.000002) 
		GPIO.output(TRIG, 0) 

		while GPIO.input(ECHO) == 0 :
			a = 0 
		time1 = time.time()
		while GPIO.input(ECHO) == 1:
			a = 1
		time2 = time.time()

		during = time2 - time1
		return during * 340 /2 * 100

	def loop(self) :
		while True:
			self._distance = self.distance()
			#self._distance = dis
			time.sleep(0.3) 


	def startWorking(self) :
	
		_thread.start_new_thread( self.loop, () ) 
