# -----------------------------------------------------------------------------
# client_02.py
# 
# Created by: Christopher Ruediger
# Date: 06.16.17
# Project: SURF 2017
# 
# This is the second version of the CLIENT that will be implemeneted on our 
# system. This client will have the following reponsibilities:
# *** Using socket programming
# - Connect to the system server (V1)
# - Accepting commands from the server via socket
# - Translate those commands to car actions
# -----------------------------------------------------------------------------

	# Needed modules
import socket
import sys
from protomod2_0 import InitRobo

	# Import pertinent modules.
import RPi.GPIO as GPIO
import motor
import car_dir
import video_dir


	# Gloabal variables
MAX2RECV = 1024
host = ''
port = 30000
server_addr = (host, port) 
packet = None


def main() :
	car_setup()
	client_socket = estClient()
	server_socket = connectToServer(client_socket) 
	try : 
		communications(server_socket) 
		
	except KeyboardInterrupt :
		cleanExit(server_socket) 
	
	
def car_setup() :
	global camActions		# Make the action dictionaries global
	global carActions
	video_dir.setup(busnum=busnum) 
	car_dir.setup(busnum=busnum)
	motor.setup(busnum=busnum)     
	video_dir.home_x_y()
	car_dir.home()
	motor.setSpeed(25)		# Set the car speed to number
	carActions = _defineCarActions()		# Define the action dictionaries
	camActions = _defineCamActions()
	
	
def _defineCarActions() :
	commands = {
		'go': motor.forward, 
		'back': motor.backward,
		'left': car_dir.turn_left,
		'right': car_dir.turn_right,
		'stop': motor.stop,
		'home': car_dir.home
		}
	return commands
	
def _defineCamActions() :
	commands = {
		'horz_left': video_dir.move_increase_x,
		'horz_right': video_dir.move_decrease_x,
		'vert_up': video_dir.move_increase_y,
		'vert_down': video_dir.move_decrease_x,
		'home': video_dir.home_x_y 
		}
	return commands
	
	
	# Establish the client socket and return it.
def estClient() :
	print("Creating client...") 
	newSocket = socket.socket()		# Create a new socket for the client
	return newSocket
	
	# Connect client to the server via the servers address
def connectToServer(client) :
	print("Connecting to server...")
	client.connect(server_addr) 	# Connect to the server 
	return client
	
def communications(theSocket) :
	sendinit(theSocket)
	
	while True:
		data = recvData(theSocket) 
		if data: 
			executepacket(data, curSocket) 
			
		else :
			print("Server closed me")
			cleanExit(theSocket) 
			
			
		
	# Decode data recieved from "socket" and return it
def recvData(socket) :
	print("*******************")
	print("Waiting...") 
	rawData = socket.recv(MAX2RECV)	# Recieve all data from given socket
	data = rawData.decode() 		# Decode the encrypted data
	return data
	
def cleanExit(server) :
	print("Connection closing...")
	server.close() 
	print("Goodbye") 
	exit()
	
    # Call the function indicated by a given input      
def callFunction(thing, action) :
	if action in carActions or action in camActions :
		if thing == 'car' :
			fnc = carActions[action]
		elif thing == 'cam' :
			fnc = camActions[action]
		fnc()
		print("\nExecuted \"", action.upper(), "\"\n") 
	else :
		print("\nUnkown action recived...\n") 
	   

def sendinit(server) :
	global packet
	
	deviceList = ['car', 'cam']
	packet = InitRobo(deviceList)
	rawdata = packet.makeJSON()
	crypticdata = rawdata.encode()		# Encode plain text data
	server.send(crypticdata) 		# Send encrypted data
	print("Data Sent.") 
	
	
	# Execute the packet recieved based off of its purpose,
	# Indicated by data field type
def executepacket(data, socket) :
	packet.setJSON(data) 
	comm_type = packet.findvalue('type') 
	if comm_type == 'cmnd' :
		thing = packet.findvalue('thing')
		action = packet.findvalue('action') 
		callFunction(thing, action) 
	elif comm_type == 'resp' :
		recvresp(data) 
	else :
		print("TYPE not yet supported.") 
		
		
def recvResp(response) :
	packet.setJSON(response) 
	code = packet.findvalue('code') 
	if code == 100 :
		print("Success:", code) 
	else :
		print("Error:", code) 
		
main()
	
	