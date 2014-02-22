from weather import *
import hexanhome.models

class HomeWatcher(object):
	"""docstring for HomeWatcher"""
	def __init__(self):
		super(HomeWatcher, self).__init__()

	def getTime(self):
		now = datetime.datetime.now()
		return now.hour + now.minute + now.second()

	def getWeekday(self):
		now = datetime.datetime.now()
		return now.weekday()

	def getTemperature(self, idCapteur):
		capteur = hexanhome.models.Capteur.objects.filter(identifiant=idCapteur)
		print(capteur)
		print(dir(capteur))
		attributs = capteur.attr_capteur_set.all
		for att in attributs:
			if att.nom == 'temperature':
				return att.valeur
		return None
		
	def getWeatherCondition(self):
		wd = WeatherDownloader('Lyon')
		condition = wd.getCurrentWeatherData().weather_condition
	
	def getPresence(self, idCapteur):
		capteur = hexanhome.models.Capteur.objects.filter(identifiant=idCapteur)
		attributs = capteur.attr_capteur_set().all()
		for att in attributs:
			if att.nom == 'presence':
				return att.valeur
		return None

