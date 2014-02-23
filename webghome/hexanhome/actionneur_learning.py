import socket

# Return a fictive ID based on id parameter
def getFictiveButtonId (id):
	firstPart = 'FF9F'
	secondPart = str(id).zfill(4)
	ID = firstPart+secondPart
	return ID
	
def getTrameON (id):
	firstPart = 'A55A6B05'
	dataBytes = '70000000'
	idBytes = id
	endPart = '30FF'
	completeTrame = firstPart+dataBytes+idBytes+endPart
	return completeTrame
	
def getTrameOFF (id):
	firstPart = 'A55A6B05'
	dataBytes = '90000000'
	idBytes = id
	endPart = '30FF'
	completeTrame = firstPart+dataBytes+idBytes+endPart
	return completeTrame
	
# ATTENTION A BIEN PASSER UNE LISTE ! 
def sendTrameToServer (trameList):
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server_adress = ('localhost', 5050)
	sock.connect(server_adress)
	data = sock.recv(50)
	if (data == 'CONNECTION OK'):
		sock.send('START')
		data = sock.recv(50)
		if (data == 'NEXT'):
			for trame in trameList:
				sock.send(trame)
				sock.recv(50)				
			sock.send('END')
	sock.close()
