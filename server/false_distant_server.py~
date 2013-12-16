import socket
import sys

#Create TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Bind socket to port
#server_adress = ('134.214.105.28', 5000)
server_adress = ('localhost', 5000)
print >>sys.stderr, 'Connecting up on %s port %s' % server_adress
sock.bind(server_adress)

#Socket listening to connections
sock.listen(1)

connection = None

#While there is no connection
while connection is None :
  print >>sys.stderr, 'waiting for connections'
  connection, client_adress = sock.accept()

print >> sys.stderr, 'connection from', client_adress
i=0

#Simulation
while True:
  data = 'Test %s' % i
  i = i+1
  connection.sendall(data)