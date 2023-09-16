# -----------------------------------------------------------------------------
# server_module.py
# 
# Created by: Christopher Ruediger
# Date: 07.05.17
# Project: SURF 2017
# 
# This module will contain a class to support a server object within our system.
# The class Server can be instantiated to act as the running server within which
# will control the communications for the system.
# -----------------------------------------------------------------------------

import socket
import select 
import sys
from protomod2_0 import *
import time
import _thread


# Global Constants
MAX2RECV = 1024

	# Server class
class Server :
	
		# Initialization for class object
	def __init__(self, hostname, portnumber) :
		
			# This is the network socket attribute
		self._server = self.setup(hostname, portnumber) 
			# This is the network packet attribute 
		self._packet = DataPack()
		self._view4packets = None
		
			# Attributes to refer to connected peripherals
		self._theRobot = True 
		#self._roboDevices = None
		self._roboDevices = ['car', 'cam', 'ultra', 'motion']
		
		self._theController = None
		self._theViews = []
			
			# Inputs to listen from 
		self._inputs = [self._server, sys.stdin]
			
			# Client whose packet is being processed
		self._curClient = None
		
		# Method to run the server operations
	def run(self) :
		try: 
			
			self.communications() 
			
		except KeyboardInterrupt:
			
			self.cleanExit() 
		
		# Setup the server socket and return
	def setup(self, host, port) :
		
			# Create a new socket
		newSocket = socket.socket()	
		
			# Allow reuse of socket # address binding
		newSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		
			# Bind to server address
		newSocket.bind((host, port))	
			
			# Listen for up to 5 connections
		newSocket.listen(5)		
			
			# Return the new socket for server use
		return newSocket

		# Define the communications for the server
	def communications(self) :
		
		_thread.start_new_thread( self.viewUpdater, () ) 
		
		while True :
		
				# Readable - arrivalls
			readable, w, e = select.select(self._inputs, [], [])	
		
				# For each arrived input
			for curSocket in readable : 
			
					# If a client has arrived for connection
				if curSocket == self._server :
					newClient = self.acceptClient()		# Accept the client
				 
					# If input is from standard input...
				elif curSocket == sys.stdin :
					userin = input()		# Get the arrived input
					print("STDIN recieved... do nothing")
				
					# If input is from client socket...
				else :
					self._curClient = curSocket
					data = self.recvData()	# Recv and process data
					self._curClient = None
				
				
	def sendPacket(self, socket = None) :
		
			# Create JSON string with packet
		rawdata = self._packet.makeJSON()
		
			# Encode plain text JSON string
		crypticdata = rawdata.encode()		
			
		if socket :
			socket.send(crypticdata) 
		
		else :
			self._socket.send(crypticdata) 	
				
		# A client connection has arrived. Accept it and return connection.
	def acceptClient(self) : 
		connection, addr = self._server.accept()		# Accept a connection 
													# connection = socket
													# addr = where it came from
		print("Recieved connection from: ", addr) 
		self._inputs.append(connection)
			
		# Recieve the data and process it 
	def recvData(self) :
		print("*******************")
		
			# Recieve all data from given socket
		rawData = self._curClient.recv(MAX2RECV)	
		
			# Decode the encrypted data
		data = rawData.decode() 		
			
			# If data is true it needs to be processed to fulfill its purpose
		if data :
			self.executepacket(data)
			
			# Otherwise it is signaling a closed connection
		else :
			self.setAvailable() 
			self._inputs.remove(self._curClient) 
			self._curClient.close()	# Close client connection
			
			
			# This will relieve the attribute that was refering to the closed
			# socket
	def setAvailable(self) :

		if self._curClient is self._theRobot : 
			self._theRobot = None
			self._roboDevices = None
			print("** The Robot has disconnected **") 
			
		elif self._curClient is self._theController :
			self._theController = None
			print("** The Controller has disconnected **") 
			
		elif self._curClient in self._theViews :
			self._theViews.remove(self._curClient) 
			print("** A VIEW has disconnected **") 
		 
			
		
			
		# Exit the program after closing all sockets
	def cleanExit(self) :
		for socket in self._inputs :
			socket.close() 
			self._inputs.remove(socket) 
		print("Goodbye") 
		exit()							# End program
			
			
		# Execute the packet recieved based off of its purpose,
		# Indicated by data field "type"
	def executepacket(self, data) :
			
			# Set my packet attribute as the recieved data
		self._packet.setJSON(data) 
		
			# Find the type of data in the packet
		comm_type = self._packet.findvalue('type') 
		
			# Initialization packet
		if comm_type == 'init' :
			self.recvinit()
				
			# Command packet
		elif comm_type == 'cmnd' :
			self.relaycmnd() 
			
			# Response packet
		elif comm_type == 'resp' :
			self.recvResp() 
			
		elif comm_type == 'alert' :
			if self._packet.findvalue('state')['Alarmed'] :
				print("ALARM") 
			else :
				print("ALARM CLEARED") 
				
			# Unknown data "type"
		else :
			print("TYPE not yet supported.") # ERROR 501?
			self.sendError(501)
			
		
		# Initialization and helpers ------------------------------------------
		
		# Recieve and initialization packet
	def recvinit(self) :
		
			# Find the thing from which the data came 
		thing = self._packet.findvalue('thing') 
			
			# If it is a client identify which type : controller or view
			# call the corresponding helper function to accept init
		if thing == 'client' :
			which = self._packet.findvalue('which') 
			if which == 'ctrl' :
				self.connectController()
			elif which == 'view' :
				self.connectView()
			else :
				print("WHICH not yet supported.")  # ERROR 503
					# Unsupported which
				self.sendError(503)
				time.sleep(.1) 
					# Failed initialization 
				self.sendError(521)
				self._inputs.remove(self._curClient) 
				self._curClient.close() 
			
			# If it is a robot call connectRobot()
		elif thing == 'robot' :
			self.connectRobot()
	
			# Otherwise it is and unknown data "thing
		else :
			print("THING not yet supported.") # ERROR 502?
				# Unsuported thing
			self.sendError(502)
			time.sleep(.1) 
				# Failed initialization 
			self.sendError(521)
			self._inputs.remove(self._curClient) # Remove this socket from inpts
			self._curClient.close() # Close its connection
		
		# Connect a controller type client
	def connectController(self) :
		
			# If the controller attribute is available assign this socket to it
		if not self._theController :
			self._theController = self._curClient	# Assign
			print("Connected a new CONTROLLER.")	# Display status
			self.sendError(100, "OK")							# Send success code
			
			# Else there already exists a controller client
		else :
			print("A CONTROLLER is already connected.") # ERROR 511?
				# Controller already connected
			self.sendError(511, "CTRL_CONN")
			time.sleep(.1) 
				# Failed initialization 
			self.sendError(521, "FAILED_INIT")
			self._inputs.remove(self._curClient) 
			self._curClient.close()   
			
		# Connect a view type client
	def connectView(self) :
	
			# If there are less than X number views accept client
			# and add to views attribute list
		if len(self._theViews) < 2 :
			self._theViews.append(self._curClient)	# Add
			print("Connected a new VIEW.")			# Display status
			self.sendError(100, "OK")							# Send success code
		else :
			print("Already 2 VIEWS connected.") # ERROR 512?
				# All views already connected
			self.sendError(512, "VIEW_CONN")
			time.sleep(.1) 
				# Failed initialization 
			self.sendError(521, "FAILED_INIT")
			self._inputs.remove(self._curClient) 
			self._curClient.close() 

		# Connect a robot type client
	def connectRobot(self) :
			
			# Find the supported devices sent with this robot init packet
		self._roboDevices = self._packet.findvalue('devices') 
			
			# If the robot attribute is vacant, connect robot
		if not self._theRobot :
			self._theRobot = self._curClient	# Assign 
			print("Connected a new ROBOT.") 	# Display status
			self.sendError(100, "OK")					# Send success code
		else :
			print("A ROBOT is already connected.") # ERROR 513
				# A robot is already connected
			self.sendError(513, "ROBO_CONN")
			time.sleep(.1) 
				# Failed initialization 
			self.sendError(521, "FAILED_INIT")
			self._inputs.remove(self._curClient) 
			self._curClient.close() 
	
	
# Command Relays and helpers ------------------------------------------

			# Failed initialization code : 521

	def relaycmnd(self) :
		
		# Peek as to what the cmnd is, if it is query for system reply.
		thing = self._packet.findvalue('thing') 
		if thing == 'system' :
			action = self._packet.findvalue('action') 
			if action == 'get' :
				state = self.generateSysState()
				self._packet = RespPack(200, "Qry_Resp", 'system', state)
				self.sendPacket(self._theController)
				print("Status sent")  
				
			
		else :
			
			if self._theRobot :
				self.sendPacket(self._theRobot)	
				print("Data Sent to robot.") 
			else :
				self.sendError(530, "NO_ROBO")
				
	def generateSysState(self) :
		state = {}
		if self._theRobot :
			state['robot'] = True 
			state['devices'] = self._roboDevices
			state['robot_state'] = { 'device1' : 'something' }#generateDeviceState() 
		else :
			state['robot'] = False 
			
		if self._theController :
			state['controller'] = True
		else :
			state['controller'] = False 
			
		if self._theViews :
			state['views'] = len(self._theViews) 
		else :
			state['views'] = False 
			
		return state

# Response Parser  -----------------------------------------
		
		# Recieve a response type packet
	def recvResp(self) : 
		
			# Get the associated code
		code = self._packet.findvalue('code') 
			# Display message according to code
		if code == 100 :
			print("Success:", code) 
		else :
			if self._curClient is self._theRobot and self._theController :
				self.sendPacket(self._theController)
			
			if code == 200 :
				print("State data sent to controller/views") 
			else :
				print("Error sent to controller/views") 
				print("Error:", code) 

# Other ---------------------------------------------------------------

		# Send an ERROR packet with code specified											
	def sendError(self, code, msg) :					
		packet = RespPack(code, msg)			
		rawdata = packet.makeJSON() 				
		crypticdata = rawdata.encode() 
		self._curClient.send(crypticdata) 
		print("Error code:", code, "sent") 
		
		
		
	def viewUpdater(self) :
		while True :
			if self._theViews :
				time.sleep(3) 
				state = self.generateSysState()
				for view in self._theViews :
					packet4views = AlertPack('system', state) 
					rawdata = packet4views.makeJSON()
					crypticdata = rawdata.encode()		
					view.send(crypticdata) 
			else :
				pass
					
		
		
		
		
		

	
		
		