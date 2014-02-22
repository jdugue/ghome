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
