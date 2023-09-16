from socket import *
from time import sleep

HOST = '10.10.67.62'
PORT = 30000
BUFSIZ = 1024
ADDR = (HOST, PORT) 

sock = socket(AF_INET, SOCK_STREAM)
sock.connect(ADDR) 

print("SOCKET CONNECTED") 
print("Closing...")
sleep(5)

sock.close()
exit()


