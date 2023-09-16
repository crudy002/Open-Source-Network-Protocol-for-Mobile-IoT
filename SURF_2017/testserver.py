from socket import *
from time import sleep

HOST = ''
PORT = 30000
BUFSIZ = 1024

sock = socket(AF_INET, SOCK_STREAM)
sock.bind((HOST, PORT))
sock.listen(5)

cliSock, addr = sock.accept()
print("SOCKET CONNECTED FROM :", addr)
print("Closing...")
sleep(5)

cliSock.close()
sock.close()
exit()
