
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

	


def main() :
	setup()
	usrIn = raw_input()
	while True :
		if usrIn == "forward" :
			motor.forward()  
		else :
			print("Invalid Selection") 
		usrIn = raw_input() 
def setup() :
	video_dir.setup(busnum=busnum) 
	car_dir.setup(busnum=busnum)
	motor.setup(busnum=busnum)     # Initialize the Raspberry Pi GPIO connected to the DC motor. 
	video_dir.home_x_y()
	car_dir.home()
	motor.setSpeed(50)


main()	
	
	
	


