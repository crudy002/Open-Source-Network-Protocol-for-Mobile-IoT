# test.py


import pygame



def main() :

	commandDict = {1: command1(), 2: command2()}
	commandDict[1]
	commandDict[2]
	keyrelease() 
	
	
def command1() :
	print("this is the FIRST command") 
	
	
def command2() :
	print("this is the SECOND command") 
	
def keyrelease() :
	pygame.init()
	firstCall = True

	pygame.key.set_repeat(1,50)
	
	try :
		while True:
			for event in pygame.event.get():
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_w:
						if firstCall :
							print('go forward')
							firstCall = False 
					elif event.key == pygame.K_s:
						print('go backward')
				elif event.type == pygame.KEYUP:
					print('stop')
					firstCall = True
						
	except KeyboardInterrupt:
		pass
	
	
main()