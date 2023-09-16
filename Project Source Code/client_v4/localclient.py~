# -----------------------------------------------------------------------------
# localclient.py
#
# Created by: Chris Ruediger
# Date: 06.09.17
#
# This is a client to be run locally to support Sunfounder Video Car Kit for 
# Raspberry Pi. It will run the robot without a network component and run using
# user input in the terminal for instruction. Right now this doesn not include 
# video.
# -----------------------------------------------------------------------------

import RPi.GPIO as GPIO
import motor
import car_dir
import video_dir

# Global Variables 
busnum = 1
#cmnds  = {'forward': forwardWrapper, 'backward': backwardWrapper}

def printhere() :
	print("here") 

def main() :
	cmnds  = {'forward': forwardWrapper, 'backward': backwardWrapper}

	setup()

	try:
		userin = input() 
		while True:
			if userin == 'w' :
				forwardWrapper() 
			elif userin == 's' : 
				backwardWrapper()
			else:
				print("Invalid Entry!")  
			userin = input()

	except KeyboardInterrupt:
		pass


def main2() :
	cmnds  = {'forward': forwardWrapper, 'backward': backwardWrapper}

	setup()

	try:
		userin = input()
		if userin in cmnds :
			fnc = cmnds[userin]
			fnc()
			print(input) 
		else :
			print("Invalid entry") 

	except KeyboardInterrupt:
                pass
	 
		
		
def forwardWrapper() :
	cmnd = 'w'
	motor.forward()
	print('forward') 
	while cmnd != '' :
		cmnd = input()
	motor.stop()
	print('stop') 

def backwardWrapper() :
	cmnd = 's'
	motor.backward()
	print('backward')
	while cmnd != '' :
		cmnd = input()
	motor.stop()
	print('stop')	
		
def setup() :
	video_dir.setup(busnum=busnum) 
	car_dir.setup(busnum=busnum)
	motor.setup(busnum=busnum)     # Initialize the Raspberry Pi GPIO connected to the DC motor. 
	video_dir.home_x_y()
	car_dir.home()
	motor.setSpeed(50)
	
	
 					


#main()
main2()
	
	
	


