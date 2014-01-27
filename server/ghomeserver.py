import socket
import datetime
import sys
import re
import MySQLdb
import ConfigParser

class Trame:
	def __init__(self, trame):
		if (len(trame) == 14):
			self.sync = trame[:4]
			self.hseq = trame[4:6]
			self.org = trame[6:8]
			self.data_bytes = trame[8:16]
			self.id_bytes = trame[16:24]
			self.status = trame[24:26]
			self.checksum = trame[26:28]
			
		def getsync(): return self.sync
		def gethseq(): return self.hseq
		def getorg(): return self.org
		def getdb(): return self.data_bytes
		def getid(): return self.id_butes
		def getstatus(): return self.status
		def getchecksum(): return self.checksum
		
class Database:
	def __init__(self):
		configParsed = ConfigParser.ConfigParser()
		configParsed.read('configdb.cfg')
		connectString = configdb.get('database_info','connectString')
		self.db = MySQLdb.connect(connectString)
		
	def execute (request):
		cursor = self.db.cursor()
		cursor.execute(request)
		result = self.cursor.fetchall()
		cursor.close()
		return result
		
	def closedb ():
		self.db.close()
		
		

def traiterTrame (trame):
	Trame tr = Trame(trame)
	if trameIdentifiee(trame):
		majDonnees(trame)
		
		
def trameIdentifiee (trame):
	# Déterminer si l'identifiant de la trame est dans la base de données
	return True

def majDonnees(trame):
	# Mettre à jour la base de données avec les données de la trame

