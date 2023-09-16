# -----------------------------------------------------------------------------
# client_module.py
# 
# Created by: Christopher Ruediger
# Date: 06.27.17
# Project: SURF 2017
# 
# This module will contain multiple classes to support client objects within
# our system. There will be a main client class that won't be called directly,
# but rather used to inherit functionality. This will decrease redundant code 
# and provide a better structured Object-Oriented system.
# -----------------------------------------------------------------------------

import socket
import select 
import sys
from protomod2_0 import *



# Global Constants
MAX2RECV = 1024

	# Super client class
class Client :
	
		# Initialization for super class
	def __init__(self) :
		
			# This is the network socket attribute
		self._socket = None 
			# This is the network packet attribute 
		self._packet = None
		
		# General setup method that will create client socket
		# accepting serverAddrr : a TUPLE - (hostnumber, portnumner) 
	def setup(self, serverAddr) :
		
			# Create a new socket
		newSocket = socket.socket()				
		
			# Try to connect it to the server
			# ??????
		fail = newSocket.connect_ex(serverAddr)	
		
			# If connection wasn't succesful print error
		if fail :
			print("Socket couldn't connect to %s @ port %d" % \
				(serverAddr[0], serverAddr[1]))
			exit()
			
			# Set the attribute socket to the newly defined/connected socket
		self._socket = newSocket 
		
		# 
	def sendPacket(self) :
		
			# Assert that a socket has been established
		assert self._socket is not None, "Socket setup failure"
		
			# Create JSON string with packet
		rawdata = self._packet.makeJSON()
		
			# Encode plain text JSON string
		crypticdata = rawdata.encode()		
			
			# Send encrypted JSON string to server
		self._socket.send(crypticdata) 		
		
		
	def communications(self, inputs) :
		
		try: 
		
			while True :
				readable, w, e = select.select(inputs, [], []) 
			
				for curSocket in readable :
				
					if curSocket == self._socket :
						data = self.processData() 
					
					elif curSocket == sys.stdin :
						userin = input() 
						self.processCmnd(userin) 
						
					elif curSocket is self._pipe :
						alarm = self._pipe.recv()
						self.sendAlert('motion', {'Armed':True, 'Alarmed': True})
						
						 
						
		except KeyboardInterrupt:
			
			self.cleanExit() 
			

	def processData(self) :
		print("*******************")
		
			# Recieve all data from given socket
		rawData = self._socket.recv(MAX2RECV)	
		
			# Decode the encrypted data
		data = rawData.decode() 		
		
		if data :
			self._packet.setJSON(data) 
			self.processPacket()
			
		else :
			print("Server closed socket...") 
			self.cleanExit()
			
			
		# Execute the packet recieved based off of its purpose,
		# Indicated by data field type
	def processPacket(self) :
		comm_type = self._packet.findvalue('type') 
		
		if comm_type == 'cmnd' :
			
			self.recvCmnd()
			
		elif comm_type == 'resp' :
			
				# Get the code that came along with the packet
			code = self._packet.findvalue('code') 
			self.recvResp(code) 
			
		else :
			self.sendError(501, "BAD_TYPE")
			print("TYPE not yet supported.") 
			
		
			# Recieve a response type packet
	def recvResp(self, code) : 
			# Display message according to code
		if code == 100 :
			print("Successful Connection:", code) 
		elif code == 200 :
			thing = self._packet.findvalue('thing')
			state = self._packet.findvalue('state')
			msg = self._packet.findvalue('msg') 
			print( state, msg ) 
		else :
			print("Error:", code) 
			message = self._packet.findvalue('msg') 
			print(message) 
		
		
	def cleanExit(self) :
		print("Connection closing...")
			# Close the communication socket
		self._socket.close() 
		print("Goodbye") 
			# Exit the program
		exit()
		
		
		# General call to main logic sequence for a client
	def run(self) :  
		
		self.communications([self._socket, sys.stdin]) 
			
	def processCmnd(self, string) :
		print("Cannot send commands") 
		
	def recvCmnd(self) :
		print("Cannot receive commands")
	
		# Send an ERROR packet with code specified											
	def sendError(self, code, msg) :					
		packet = RespPack(code, msg)			
		rawdata = packet.makeJSON() 				
		crypticdata = rawdata.encode() 
		self._curClient.send(crypticdata) 
		print("Error code:", code, "sent") 
		
		
# -------------------------- Controllers and Views --------------------------
	
class View(Client) :
	
	def __init__(self, hostname, portnum, which = 'view') :
		super().__init__() 
		self.setup(hostname, portnum, which)
		self._devices = None
			
	def setup(self, host, port, which) :
		super().setup((host, port)) 
		self.sendInit(which)
			
	def sendInit(self, which) :
		self._packet = InitClient(which)
		super().sendPacket() 
		
	def displayStates(self) :
		pass
		
		 
	
class Controller(View) :
	
	def __init__(self, hostname, portnum) :
		super().__init__(hostname, portnum, 'ctrl')
		 
	def processCmnd(self, string) :
		newstr = string.split()
		if len(newstr) == 1 :
			self._packet = CmndPack('car', newstr[0])
		elif len(newstr) == 2 :
			self._packet = CmndPack(newstr[0], newstr[1])
		else :
			self._packet = CmndPack(newstr[0], newstr[1], newstr[2])
		super().sendPacket()
	
	
	
			
			
			
		
	

		
		
		
	
		
		

		