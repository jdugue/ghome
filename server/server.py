import socket
import datetime
import sys
import re
import binascii

#Create TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Bind socket to port
server_adress = ('134.214.106.23', 5000)
#server_adress = ('localhost', 5000)
print >>sys.stderr, 'Connecting up on %s port %s' % server_adress

#Connection to server
sock.connect(server_adress)

#Date du jour
now = datetime.datetime.now()

#Fichier de donnees
fichier_donnes = open("trame_capteurs_"+str(now.day)+"_"+str(now.month),"a")

#Write all receptions
while True:
  data = sock.recv(4096)
  data_struct = (data[:4], data[4:6], data[6:8], data[8:16], data[16:24], data[24:26], data[26:28])
  print >>sys.stderr, "Sync=[%s], LG=[%s], ORG=[%s], DB=[%s], ID=[%s], STATUS=[%s], CHECK_SUM=[%s]" % data_struct
  
  DB0 = bin(int(data[14:16],16))[2:]
  print "VALEUR DB0 :"
  print DB0
	
  fichier_donnes.write(data+"\n")
