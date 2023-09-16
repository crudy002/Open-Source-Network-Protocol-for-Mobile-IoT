
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
action = {'forward': motor.forward(), 'backward': motor.backward()}
	


def main() :
	setup()
	usrIn = raw_input()
	while True :
		if usrIn in action.keys() :
			repeater(action[usrIn])
		else :
			print("Invalid Selection") 
		usrIn = raw_input() 
		
		
		
def _forwardWrapper() :
	cmnd = raw_input()
	while cmnd == '\n' :
		motor.foward()
		print('forward')
		motor.stop()
		cmnd = raw_input()
		
def setup() :
	video_dir.setup(busnum=busnum) 
	car_dir.setup(busnum=busnum)
	motor.setup(busnum=busnum)     # Initialize the Raspberry Pi GPIO connected to the DC motor. 
	video_dir.home_x_y()
	car_dir.home()
	motor.setSpeed(50)
	
	
	
def repeater(function) :
	pygame.init()
	firstCall = True

	pygame.key.set_repeat(1,50)
	
	for event in pygame.event.get():
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_w:
				if firstCall :
					print('go forward')
					firstCall = False 
				elif event.key == pygame.K_s:
					print('go backward')
			elif event.type == pygame.KEYUP:
				print('stop')
				firstCall = True
					


main()	
	
	
	


