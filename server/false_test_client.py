import socket
import sys

#Create TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Bind socket to port
#server_adress = ('134.214.106.23', 5000)
server_adress = ('localhost', 5000)
print >>sys.stderr, 'Connecting up on %s port %s' % server_adress

#Connection to server
sock.connect(server_adress)

#Write all receptions
while True:
  data = sock.recv(2048)
  print >>sys.stderr, '%s' % data