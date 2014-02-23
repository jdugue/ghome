#-*- coding: utf-8 -*-

import socket
import time
import datetime
import sys
import re
import MySQLdb
import ConfigParser
from thread import *
import requests

class Trame:
	def __init__(self, trame):
		if (len(trame) == 28):
			self.sync = trame[:4]
			self.hseq = trame[4:6]
			self.org = trame[6:8]
			self.data_bytes = trame[8:16]
			self.id_bytes = trame[16:24]
			self.status = trame[24:26]
			self.checksum = trame[26:28]
		
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
			print request
			cursor.execute(request)		
			self.db.commit()
			return True
		except MySQLdb.Error, e:
			self.db.rollback()
			print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
			return False


	def isIdPresentOnDb(self, id):
		# Renvoit False, si pas pu se connecter ou si pas dans la base
		self.db = self.connectDb()
		if(self.db):
			request = "SELECT identifiant FROM hexanhome_capteur WHERE identifiant='{0}';".format(id)
			resultCapteur = self.executeQuery(request)
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
			updateRequest = "UPDATE hexanhome_attribut SET valeur={0} WHERE identifiant='{1}' AND nom='{2}'".format(value,idCapteur,name)
			self.executeUpdate(updateRequest)
			self.db.close()
	
	def getIdTypeByIdCapteur(self, idCapteur):
		self.db = self.connectDb()
		if(self.db):
			getRequest = "SELECT capteurtype FROM hexanhome_capteur WHERE identifiant='{0}'".format(idCapteur)
			result = self.executeQuery(getRequest)
			self.db.close()
			return result[0][0]
			
	def getValeurFromCapteur(self, idCapteur):
		self.db = self.connectDb()
		if(self.db):
			getRequest = "SELECT valeur FROM hexanhome_attribut WHERE identifiant='{}'".format()
			result = self.executeQuery(getRequest)
			self.db.close()
			return [0][0]

def parseTemperatureFromTrame(data_trame):
	# Récupère la valeur de température depuis la partie Data d'une trame de capteur 0.40
	return 40*int(data_trame[4:6],16)/255
	
def parseContactFromTrame(data_trame):
	# Renvoie 0 si le contacteur est "open" ou 1 si il est "close"
	DB0 = bin(int(data_trame[6:8],16))[2:].zfill(8)
	return DB0[7]
	
def trameIdentifiee (trame, database):
	# Déterminer si l'identifiant de la trame est dans la base de données
	return (database.isIdPresentOnDb(trame.id_bytes))
	
def majDonnees(trame, database, profileManager):
	# Mettre à jour la base de données avec les données de la trame
	if (database.getIdTypeByIdCapteur(trame.id_bytes) == 'C'):
		database.updateValueForCapteur(trame.id_bytes, parseTemperatureFromTrame(trame.data_bytes),"temperature")
	elif (database.getIdTypeByIdCapteur(trame.id_bytes) == 'F'):
		database.updateValueForCapteur(trame.id_bytes, parseContactFromTrame(trame.data_bytes), "contact")
	profileManager.testProfiles()

class ProfileGesture:
	def __init__(self, date):
		self.lastTest = self.timestamp(date)
		
	def launchThreadTestProfiles(self):	
		start_new_thread(self.callTestProfilesEveryMinutes,())
		
	def callTestProfilesEveryMinutes(self):
		while True:
			sleeptime = 60 - datetime.datetime.now().second
			time.sleep(sleeptime)
			self.testProfiles()
			
	def testProfiles (self):
		if (self.timestamp(datetime.datetime.now()) - self.lastTest != 0):
			url = 'http://127.0.0.1:8000/test_profiles/'
			params = {'email':'vincent.durif@insa-lyon.fr', 'password': 'pwd', 'port':'5000'}
			r = requests.post(url, data=params)
			self.lastTest = self.timestamp(datetime.datetime.now())
	
	def timestamp (self, date):
		return time.mktime(date.timetuple())
		

def traiterTrame(trame, profileManager):
	tr = Trame(trame)
	DB = Database()
	
	if trameIdentifiee(tr, DB):
		majDonnees(tr, DB, profileManager)

def printInAFile (text):
	file_object = open('DEBUG.txt', 'w')
	file_object.write(text)
	file_object.close()

def threadSender (socket_rcv, socket_snd):
	while True:
		connection, client_adress = socket_rcv.accept()
		data = connection.recv(28)
		if (data == 'START'):
			while ((data = connection.recv(28)) != 'END'):
				printInAFile(data)
				#socket_snd.send(data)
		connection.close()
		
################## COMMUNICATION ACTIONNEURS #######################
def listenTrameServer ():
	sock_listen = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server_adress_listen = ('localhost',5050)
	sock_listen.bind(server_adress_listen)
	sock_listen.listen(5)

	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	#server_adress = ('134.214.106.23', 5000)
	server_adress = ('127.0.0.1', 5000)
	sock.connect(server_adress)
	
	start_new_thread(threadSender,(sock_listen,sock,))
	
	profileManager = ProfileGesture(datetime.datetime.now())
	profileManager.launchThreadTestProfiles()

	#Write all receptions
	while True:
		data = sock.recv(28)
		print "%s" % data
		if (len(data) == 28):
			start_new_thread(traiterTrame,(data,profileManager,))
####################################################################

if __name__ == '__main__':
	listenTrameServer ()
