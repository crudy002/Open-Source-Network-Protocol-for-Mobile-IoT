# -----------------------------------------------------------------------------
# client_01.py
# 
# Created by: Christopher Ruediger
# Date: 06.25.17
# Project: SURF 2017
# 
# This is intended to become the controller as of now it is a client 
# that connects to server and recvs responses.
# -----------------------------------------------------------------------------

	# Needed modules
import socket
import sys
import select
from protomod2_0 import InitClient # , CtrlPack, RespPack

	# Gloabal variables
MAX2RECV = 1024
host = ''
port = 30001
server_addr = (host, port) 
packet = None


def main() :
	
	client_socket = estClient()
	server_socket = connectToServer(client_socket) 
	try : 
		communications(server_socket) 
		
	except KeyboardInterrupt :
		cleanExit(server_socket) 
	
	
		
	
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
	
	inputs = [theSocket, sys.stdin]		# Listen to the conn and stdin
	

	while True :
		
		readable, w, e = select.select(inputs, [], [])	# Readable - arrivalls
		
		for curSocket in readable : 
	
			if curSocket == theSocket :
				data = recvData(theSocket) 
				if data: 
					recvResp(data) 
				else :
					print("Server closed me") 
					cleanExit(theSocket) 
			
			
		
	# Decode data recieved from "socket" and return it
def recvData(socket) :
	print("*******************")
	rawData = socket.recv(MAX2RECV)	# Recieve all data from given socket
	data = rawData.decode() 		# Decode the encrypted data
	return data
	
def recvResp(response) :
	packet.setJSON(response) 
	code = packet.findvalue('code') 
	if code == 100 :
		print("Success:", code) 
	else :
		print("Error:", code) 
	
def cleanExit(server) :
	print("Connection closing...")
	server.close() 
	print("Goodbye") 
	exit()
	
def sendinit(server) :
	global packet
	
	packet = InitClient('ctrl')
	rawdata = packet.makeJSON()  
	crypticdata = rawdata.encode()		# Encode plain text data
	server.send(crypticdata) 		# Send encrypted data
	print("Data Sent.") 
	
	
	
	
main()
	
	
	