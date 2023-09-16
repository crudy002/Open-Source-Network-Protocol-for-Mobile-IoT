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

# Import pertinent modules.
import RPi.GPIO as GPIO
import motor
import car_dir
import video_dir

# Global Variables 
busnum = 1

	# Main
def main() :
	global actions
	actions  = defineActions()
	setup()
	try:
		userin = input()
		if userin in actions :
			callFunction(userin)
		else :
			print("Invalid entry") 

	except KeyboardInterrupt:
		pass
	
    # Call the function indicated by a given input      
def callFunction(someinput) :
	fnc = actions[someInput]
	fnc()
	print(input) 

	# Define the actions in a dictionary to be used for easy indexing of 
	# commands for the car
def defineActions() :
	commands = {
		'forward': forwardWrapper, 
		'backward': backwardWrapper,
		'left': car_dir.turn_left,
		'right': car_dir.turn_right,
		'stop': motor.stop,
		'home': car_dir.home,
		'x+': video_dir.move_increase_x,
		'x-': video_dir.move_decrease_x,
		'y+': video_dir.move_increase_y,
		'y-': video_dir.move_decrease_x,
		'xy_home': video_dir.home_x_y 
		}
	return commands
	 
	 # Setup the servo controller and motor drivers.
def setup() :
		# Initialize the Raspberry Pi GPIO connected to the DC motor. 
	video_dir.setup(busnum=busnum) 
	car_dir.setup(busnum=busnum)
	motor.setup(busnum=busnum)     
	video_dir.home_x_y()
	car_dir.home()
	motor.setSpeed(50)
	
	# This function will call FORWARD on the motors and only stop once return
	# is entered on the cmnd line.
def forwardWrapper() :
	cmnd = 'w'
	motor.forward()
	print('forward') 
	while cmnd != '' :
		cmnd = input()
	motor.stop()
	print('stop') 

	# This function will call BACKWARD on the motors and only stop once return
	# is entered on the cmnd line.
def backwardWrapper() :
	cmnd = 's'
	motor.backward()
	print('backward')
	while cmnd != '' :
		cmnd = input()
	motor.stop()
	print('stop')
	
	# Call the main fucntion to run program.
main()

	
	
	


