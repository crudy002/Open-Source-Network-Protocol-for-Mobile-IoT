

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
	
	def __init__(self, thing, action) :
		super().__init__("ctrl") 
		self.addkeyval("thing", thing)
		self.addkeyval("action", action) 
		



# ------------------------ Response Packets --------------------------

class RespPack(DataPack) :
	
	def __init__(self, resp_code) :
		super().__init__("resp") 
		self.addkeyval("code", resp_code)  
		 



		
		
		
		
		
		
		
		
		
		
		
		
		
