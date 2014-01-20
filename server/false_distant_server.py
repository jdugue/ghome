import socket
import sys
from thread import *
import time

fichier_donnees = open("trame_capteurs_13_1","r")

#Create TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Bind socket to port
server_adress = ('localhost', 5000)
print >>sys.stderr, 'Connecting up on %s port %s' % server_adress
sock.bind(server_adress)

#Socket listening to connections
sock.listen(5)

def clientthread(conn):
	while True:
		conn.send(fichier_donnees.readline())
		time.sleep(2)
		

#While there is no connection
while True :
  connection, client_adress = sock.accept()
  start_new_thread(clientthread,(connection,))
  
connection.close()
sock.close()
