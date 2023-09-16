

import json

class DataPack :
	def __init__(self, comm_type = None) :
		if comm_type is not None :
			self._object = {'type': comm_type}
		else :
			self._object = {}
			
			
		# Returns list if all keys in object
	def getkeys(self) :
		return self._object.keys()
		
		# Returns list of all values in object
	def getvals(self) :
		return self._object.values() 
		
		# This will clear all key/value pairs from the object
	def clear(self) :
		self._object.clear() 
		
		# Return the value correspnding to the target key 
	def findvalue(self, targetkey) :
		return self._object[targetkey]
		
		# This will add or update a key with the specified value
	def addkeyval(self, key, value) :
		self._object[key] = value 
		
		# This will delete the key and its value if the key exist
		# Otherwise an assertion will be raised
	def delkey(self, key) :
		assert key in self._object, "Key not found to delete"
		self._object.pop(key) 
	
		# Str representation of the object
	def __repr__(self) :
		return str(self._object) 
		
		# Will make protocol object into a string
	def makeJSON(self) :
		return json.dumps(self._object)
		
		# This will set a JSON object as the classes protocol object
	def setJSON(self, JSONthing) :
		self._object = json.loads(JSONthing) 
		
# ---------------------- Initialization Packets -----------------------
		
class InitPack(DataPack) :
	
	def __init__(self, thing) :
		super().__init__("init") 
		self.addkeyval("thing", thing) 
		
		
class InitRobo(InitPack) :
	
	def __init__(self, devices) :
		super().__init__("robot")
		self.addkeyval("devices", devices) 
		
		
class InitClient(InitPack) :
	
	def __init__(self, which) :
		super().__init__("client")
		self.addkeyval("which", which) 
	
		
		
# ------------------------- Control Packets --------------------------

class CmndPack(DataPack) :
	
	def __init__(self, thing, action, paramlist = None) :
		super().__init__("cmnd") 
		self.addkeyval("thing", thing)
		self.addkeyval("action", action) 
		if paramlist is not None : 
			self.addkeyval("param", paramlist) 
		



# ------------------------ Response Packets --------------------------




CODE_OK = 100

BAD_TYPE = 501
BAD_THING = 502
BAD_WHICH = 503
BAD_ACTION = 504
BAD_PARAM = 505




CTRL_CONN = 511
VIEW_CONN = 512
ROBO_CONN = 513

CANT_INIT = 521

MAX_SPEED = 551
MIN_SPEED = 552



class RespPack(DataPack) :
	
	def __init__(self, resp_code, message, device = None, statelist = None) :
		super().__init__("resp") 
		self.addkeyval("code", resp_code)  
		self.addkeyval("msg", message)
		if device is not None :
			self.addkeyval("thing", device)
		if statelist is not None :
			self.addkeyval("state", statelist)
			
			
			
			
# ----------------------- Info Pack ----------------------------

class AlertPack(DataPack) :
	
	def __init__(self, device, statelist) :
		super().__init__("alert") 
		self.addkeyval("thing", device) 
		self.addkeyval("state", statelist) 
			

		
		
		 

