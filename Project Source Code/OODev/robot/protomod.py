# -----------------------------------------------------------------------------
# protomod.py
#
# Created by: Chris Ruediger
# Date: 06.09.17
#
# This is a module that will establish a class which can be instantiated by a 
# node within a given system which will represent a JSON object similair to a 
# dictionary. This Object will be utilized to carry out the Network Protocol 
# established to faciliate communicates within that given system.
# -----------------------------------------------------------------------------

import json

# json.dumps(Non-JSON Object)	-- JSON encoding
# json.load(JSON Object)		-- JSON decoding



class DataPack :

	def __init__(self) :
		self._object = {}
		
		# Return the current object w/ key,val pairs
	def getDict(self) :
		return self._object
		
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
	def findvalue(targetkey) :
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
		