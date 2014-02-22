def getFictiveButtonId (id):
	firstPart = 'FF9F'
	secondPart = str(id).zfill(4)
	ID = firstPart+secondPart
	return ID
