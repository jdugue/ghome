from weather import *
import datetime
import hexanhome.models

class HomeWatcher(object):
	"""docstring for HomeWatcher"""
	def __init__(self):
		super(HomeWatcher, self).__init__()

	def getTime(self):
		#Hour as string
		now = datetime.datetime.now()
		return str(now.hour)+':'+str(now.minute)

	def getWeekday(self):
		now = datetime.datetime.now()
		return now.weekday()

	def getTemperature(self, idCapteur):
		capteur = hexanhome.models.Capteur.objects.get(identifiant=idCapteur)
		attributs = capteur.attr_capteur_set.all()
		for att in attributs:
			if str(att.id_attr) == 'temperature':
				return att.id_attr.valeur
		return None
		
	def getWeatherCondition(self):
		wd = WeatherDownloader('Lyon')
		condition = wd.getCurrentWeatherData().weather_condition
		return condition
	
	def getPresence(self, idCapteur):
		capteur = hexanhome.models.Capteur.objects.get(identifiant=idCapteur)	
		attributs = capteur.attr_capteur_set.all()
		for att in attributs:
			if str(att.id_attr) == 'presence':
				return att.id_attr.valeur
		return None

