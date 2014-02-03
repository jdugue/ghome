#-*- coding: utf-8 -*-

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
		configParser = ConfigParser.ConfigParser()
		configParser.read('configdb.cfg')
		self.host = configParser.get('database_info','host')
		self.user = configParser.get('database_info','user')
		self.passwd = configParser.get('database_info','passwd')
		self.db_name = configParser.get('database_info','db')

	def connectDb(self):
		try:
			return MySQLdb.connect(self.host, self.user, self.passwd, self.db_name)
		except MySQLdb.Error, e:
			print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
			return False
	

	def executeQuery (self, request):
		
		cursor = self.db.cursor()
		cursor.execute(request)
		result = cursor.fetchall()
		cursor.close()
		return result

	def executeUpdate (self, request):
		cursor = self.db.cursor()
		try:
			cursor.execute(request)		
			db.commit()
			cursor.close()
			return True
		except MySQLdb.Error, e:
			db.rollback()
			cursor.close()
			print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
			return False


	def isIdPresentOnDb(self, id):
		# Renvoit False, si pas pu se connecter ou si pas dans la base
		self.db = self.connectDb()
		if(self.db):
			resultCapteur = self.executeQuery('SELECT identifiant FROM hexanhome_capteur WHERE identifiant={0};'.format(id))
			resultActionneur = False # self.execute('SELECT id_piece_id FROM hexanhome_piece WHERE id={0};'.format(id))
			self.db.close()
			if (resultCapteur or resultActionneur):
				return True
		else:
			return False

	def updateValueForCapteur(self, idCapteur, value, name):
		# Row exists when sensor is already created on the webserver
		self.db = self.connectDb()
		if(self.db):
			updateRequest = 'UPDATE hexanhome_attribut SET valeur={0} WHERE identifiant={1} AND nom={2}'.format(value,idCapteur,name)
			self.executeUpdate(updateRequest)
			self.db.close()


def traiterTrame(trame):
	tr = Trame(trame)
	if trameIdentifiee(tr):
		majDonnees(tr)
		
		
def trameIdentifiee (trame):
	# Déterminer si l'identifiant de la trame est dans la base de données
	return True

def majDonnees(trame):
	# Mettre à jour la base de données avec les données de la trame
	pass