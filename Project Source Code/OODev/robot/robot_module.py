# robot_module.py

from client_module import Client
from protomod2_0 import *
from pir_module import PIR
from ultra_module import ULTRA
from multiprocessing import Pipe

	# Import pertinent modules.
import RPi.GPIO as GPIO
import motor
import car_dir
import video_dir


# ---------------------------------- Robot ----------------------------------
	
class Robot(Client) :
	
	
		# Init for a robot object, 
		# call super init,
		# create all attributes and call setup function.
	def __init__(self, hostname, portnum) :
		
		super().__init__()
		
		self._carActions = self._defineCarActions()
		self._camActions = self._defineCamActions()
		self._motionActs = self._defineMotionActs() 
		self._ultraActs  = self._defineUltraActs()
		
			# Devices and associated attributes
		self._carDevices = None
		self._pir = None
		self._pipe = None
		self._ultra = None
		
			# Speed
		self._defaultspeed = 50 
		self._speed = 50 
		
			# Setup attributes and hardware
		self.setup(hostname, portnum)
		
		
		# Run the main logic sequence
	def run(self) :
			
		super().communications([self._socket, self._pipe]) 
			
		# Setup attributes and hardware components
	def setup(self, host, port) :
		
			# Establish connection to server and send init packet
		super().setup((host, port)) 
		self.sendInit()
		
			# Hardware setup
		busnum = 1
		video_dir.setup(busnum=busnum) 
		car_dir.setup(busnum=busnum)
		motor.setup(busnum=busnum)  
		video_dir.home_x_y() 
		car_dir.home() 
		motor.setSpeed(self._speed)	
		
			# Fulfill empty attributes
		self._carDevices = ['car', 'cam', 'motion', 'ultra']
		
			# Passive infrared (Motion)
		self._pipe, child_conn = Pipe()
		self._pir = PIR(child_conn)
		
			# Ultrasonic (Distance/Obstacle Avoidance) 
		self._ultra = ULTRA()
		
		# Send an initialization packet specific to a robot
	def sendInit(self) :
		self._packet = InitRobo(self._carDevices)
		super().sendPacket() 
	
# -----------------------------------------------------------------------------	

		# Define the possible actions for the car
	def _defineCarActions(self) :
		commands = {
			'go': motor.forward, 
			'back': motor.backward,
			'left': car_dir.turn_left,
			'right': car_dir.turn_right,
			'stop': motor.stop,
			'home': car_dir.home,
			'inc' : self.speedUp,
			'dec' : self.speedDown,
			'speed_reset' : self.resetSpeed,
			'get' : self.carGet,
			'speed_set' : self.speedSet
			}
		return commands
	
		# Reset speed speed of car to default speed
	def resetSpeed(self) :
		self._speed = self._defaultspeed
		
		# Speed the car up by incrmenet of 5
	def speedUp(self) :
		if self._speed <= 95 :
			self._speed  += 5
			motor.setSpeed(self._speed)
			print("speed =", self._speed)
		else :
			print("MAX speed reached")
			super().sendError(553, "MAX_SPD") 

		# Slow the car down by an increment of 5
	def speedDown(self) :
		if self._speed >= 20 :
			self._speed -= 5
			motor.setSpeed(self._speed) 
			print("speed =", self._speed) 
		else :
			print("MIN speed reached") 
			super().sendError(552, "MIN_SPD")

		# Get the state of the car 
	def carGet(self) :
		self.sendStatus('car', {'speed': self._speed, 'devices': self._carDevices})

		# Set the speed to a specified number within limit of 20-100
	def speedSet(self, speed) :
		speed = int(speed) 
		if speed >= 20 and speed <= 100 :
			self._speed = speed
			motor.setSpeed = speed
		else :
			super().sendError(551, "INVLD_SPD") 
			
# -----------------------------------------------------------------------------	
	
	def _defineCamActions(self) :
		commands = {
			'horz_left': video_dir.move_increase_x,
			'horz_right': video_dir.move_decrease_x,
			'vert_up': video_dir.move_increase_y,
			'vert_down': video_dir.move_decrease_x,
			'home': video_dir.home_x_y
			}
		return commands
		
# -----------------------------------------------------------------------------	

	def _defineMotionActs(self) :
		commands = {
			'arm' :	self.arm,
			'disarm' : self.disarm,
			'get' : self.getPIRState 
			}
		return commands

	def arm(self) :
		self._pir.arm()

	def disarm(self) :
		self._pir.disarm()

	def getPIRState(self) :
		armed, alarmed = self._pir.getState()  
		self.sendStatus('motion', {'armed': armed, 'alarmed':alarmed})
		
# -----------------------------------------------------------------------------	
		
	def _defineUltraActs(self) :
		commands = {
			'get' : self.getUltraState 
			}
		return commands
		
	def getUltraState(self) :
		dis = self._ultra.getDistance() 
		print(dis) 
		self.sendStatus('ultra', {'distance': dis})
	
# -----------------------------------------------------------------------------	
		
	    # Call the function indicated by a given input      
	def recvCmnd(self) :
		
		thing = self._packet.findvalue('thing')
		action = self._packet.findvalue('action')
		print(thing, action) 
		if thing == 'car' :

			if action in self._carActions :
				fnc = self._carActions[action]
				if fnc == self.speedSet :
					param = self._packet.findvalue('param') 
					fnc(param) 
				else :
					fnc()
			else :
				print("\nUnkown action recieved...\n")
				super().sendError(504)	

		elif thing == 'cam' :

			if action in self._camActions :
				fnc = self._carActions[action]
				fnc()
			else :
				print("\nUnkown action recieved...\n")
				super().sendError(504)
				
		elif thing == 'motion' :
			if action in self._motionActs : 
				fnc = self._motionActs[action]
				fnc()
			else :
				print("\nUnkown action recieved... \n") 
				super().sendError(504)
				
		elif thing == 'ultra' :
			if action in self._ultraActs : 
				fnc = self._ultraActs[action]
				fnc()
			else :
				print("\nUnkown action recieved... \n") 
				super().sendError(504)
				
		elif thing == 'robot' :
			if action == 'get' :
				self.generateFullStatus()

		else :
			print("\nUnkown thing sending command...\n") 		
		
		
	def sendStatus(self, devicename, statelist) :
		self._packet = RespPack(200, "Qry_Resp", devicename, statelist)		
		super().sendPacket()
		print("Status sent")  
		
		
	def sendAlert(self, devicename, statelist) :
		self._packet = AlertPack(devicename, statelist) 
		super().sendPacket()
		print("Alert sent") 
		
		
	def generateFullStatus(self) :
		armed, alarmed = self._pir.getState() 
		distance = self._ultra.getDistance() 
		states = {
			"car" : {'speed': self._speed},
			"cam" : None,
			"motion": {'armed': armed, 'alarmed':alarmed},
			"ultra": {'distance': distance}
		}
		
		self.sendStatus("robot", states) 
		
		
	
		
		
