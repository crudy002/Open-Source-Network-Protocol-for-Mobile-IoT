# pirtest.py

from pir_module import *
import time

mine = PIR() 

while True :
	armed, alarmed = mine.getState()
	print(armed, alarmed) 
	time.sleep(2)
