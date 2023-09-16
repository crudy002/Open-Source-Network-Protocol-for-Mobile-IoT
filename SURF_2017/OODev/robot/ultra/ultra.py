import RPi.GPIO as GPIO
import time
TRIG = 35
ECHO = 36

def setup() :

	GPIO.setmode(GPIO.BOARD) 
	GPIO.setwarnings(False) 
	GPIO.setup(TRIG, GPIO.OUT) 
	GPIO.setup(ECHO, GPIO.IN) 

def distance() :
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

def loop() :
	while True:
		dis = distance()
		print(dis, 'cm') 
		print()
		time.sleep(0.3) 

def destroy() : 
	GPIO.cleanup() 


def main() :

	setup()
	try :
		loop()
	except KeyboardInterrupt :
		destroy()

main()
