# -----------------------------------------------------------------------------
# server.py
# 
# Created by: Christopher Ruediger
# Date: 06.25.17
# Project: SURF 2017
# 
#
# -----------------------------------------------------------------------------


    # Needed modules
import socket
import sys
import select
from protomod2_0 import *

	# Global variables
MAX2RECV = 1024
host = '' 
port = 30000
server_addr = (host, port) 
packet = DataPack() 


	# - Est. Server
	# - Accept connections
	# - Proceed comminocations
	# - Once comm are over, accept new connection
	# - Program killed/cleaned up using ctrl-C
def main():
	server_socket = estServerSocket()
	try:
		
		communications(server_socket)
	except KeyboardInterrupt :
		cleanExit()
	
	# Establish a socket for the server to listen for connections. Return it.
def estServerSocket() :
	print("Creating server...") 
	newSocket = socket.socket()		# Create a new socket for the server
	print("Binding socket to", host, "on port", port) 
	newSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	newSocket.bind(server_addr)		# Bind the socket to the given server_addr
	newSocket.listen(5)				# Listen for conn from client
	return newSocket
	
	# A client connection has arrived. Accept it and return connection.
def acceptClient(serverSocket) : 
	connection, addr = serverSocket.accept()		# Accept a connection 
													# connection = socket
													# addr = where it came from
	print("Recieved connection from: ", addr) 
	return connection 
	
	
def communications(server) :
	global theRobot
	global theController
	global theViews
	global inputs 
	theRobot = None
	theController = None
	theViews = []

	
	inputs = [server, sys.stdin]		# Listen to the conn and stdin
	

	while True :
		
		readable, w, e = select.select(inputs, [], [])	# Readable - arrivalls
		
		for curSocket in readable : 
			
				# If a client has arrived for connection
			if curSocket == server :
				newClient = acceptClient(server)		# Accept the client
				inputs.append(newClient) 
			
				# If input is from standard input...
			elif curSocket == sys.stdin :
				userin = input()		# Get the arrived input
				print("STDIN recieved... do nothing")
				
				# If input is from client socket...
			else :
				data = recvData(curSocket)
				if data :
					executepacket(data, curSocket) 
	
				else :
					setAvailable(curSocket) 
					inputs.remove(curSocket) 
					curSocket.close()	# Close client connection
					

			
def setAvailable(socket) :
	global theRobot
	global theController
	if socket is theRobot : 
		theRobot = None
	elif socket is theController :
		theController = None
	elif socket in theViews :
		theViews.remove(socket) 

	
	# Deode data recieved from "socket" and return it
def recvData(socket) :
	print("Recieving data") 
	rawData = socket.recv(MAX2RECV)	# Recieve all data from given socket
	data = rawData.decode() 		# Decode the encrypted data
	return data
	
	# Exit the program after closing all sockets
def cleanExit() :
	for socket in inputs :
		socket.close() 
		inputs.remove(socket) 
	print("Goodbye") 
	exit()							# End program
	
	
	
	# Execute the packet recieved based off of its purpose,
	# Indicated by data field type
def executepacket(data, socket) :
	packet.setJSON(data) 
	comm_type = packet.findvalue('type') 
	if comm_type == 'init' :
		recvinit(socket)
	elif comm_type == 'cmnd' :
		relaycmnd(socket) 
	elif comm_type == 'resp' :
		recvresp(data) 
	else :
		print("TYPE not yet supported.") 
		
		
# Initialization and helpers ------------------------------------------
		
def recvinit(socket) :
	thing = packet.findvalue('thing') 
	
	if thing == 'client' :
		which = packet.findvalue('which') 
		if which == 'ctrl' :
			connectController(socket)
		elif which == 'view' :
			connectView(socket)
		else :
			print("WHICH not yet supported.") 
			inputs.remove(socket) 
			socket.close() 
			
	elif thing == 'robot' :
		connectRobot(socket)
	
	else :
		print("THING not yet supported.") # ERROR
		inputs.remove(socket) 
		socket.close() 
		
		
def connectController(socket) :
	global theController
	
	if not theController :
		theController = socket
		print("Connected a new CONTROLLER.") 
		sendOK(socket)
	else :
		print("A CONTROLLER is already connected.") # ERROR
		sendError(501, socket)
		inputs.remove(socket) 
		socket.close() 

def connectView(socket) :
	global theViews
	
	
	if len(theViews) < 2 :
		theViews.append(socket)
		print("Connected a new VIEW.")
		sendOK(socket)
	else :
		print("Already 2 VIEWS connected.") # ERROR
		sendError(501, socket)
		inputs.remove(socket) 
		socket.close() 

def connectRobot(socket) :
	global theRobot
	global roboDevices
	
	roboDevices = packet.findvalue('devices') 
	
	if not theRobot :
		theRobot = socket
		print("Connected a new ROBOT.") 
		sendOK(socket)
	else :
		print("A ROBOT is already connected.") # ERROR
		sendError(501, socket)
		inputs.remove(socket) 
		socket.close() 
	
	
	
	

# Command Relays and helpers ------------------------------------------

def relaycmnd(socket) :
	packet.makeJSON() 
	rawdata = packet.makeJSON()
	crypticdata = rawdata.encode()		# Encode plain text data
	if theRobot :
		#theRobot.send(crypticdata) 		# Send encrypted data
		pass
		print("Data Sent to robot.") 
	else :
		sendError(520, socket)
	
	
	
				
	# Encrypt "data" and send to "socket"
def sendData(socket, data) :
	#print("Sending \"", data, "\"") 
	rawdata = _commandHelper(data) 
	crypticdata = rawdata.encode()		# Encode plain text data
	socket.send(crypticdata) 		# Send encrypted data
	print("Data Sent.") 
	
def _commandHelper(cmnd) :
	packet.clear()
	if cmnd.startswith("x") or cmnd.startswith("y") :
		packet.addkeyval("thing",  "cam") 
	else :
		packet.addkeyval("thing", "car") 
	packet.addkeyval("action", cmnd) 
	return packet.makeJSON()


# Response Parser and helpers -----------------------------------------

def recvresp(response) :
	packet.setJSON(response) 
	code = packet.findvalue('code') 
	if code == 100 :
		print("Success:", code) 
	else :
		print("Error:", code) 

# Other ---------------------------------------------------------------


def sendOK(socket) :
	packet = RespPack(100) 
	rawdata = packet.makeJSON() 				# ^
	crypticdata = rawdata.encode() 			# |
	socket.send(crypticdata) 					# |
	print("OK response sent") 					# Possibly make these 1
														# |
def sendError(code, socket) :					# |
	packet = RespPack(code)						# |
	rawdata = packet.makeJSON() 				# v
	crypticdata = rawdata.encode() 
	socket.send(crypticdata) 
	print("Error code:", code, "sent") 
	
	
	
main()
	