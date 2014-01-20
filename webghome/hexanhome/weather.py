import requests
import json

class WeatherDownloader(object):
	"""Classe pour telecharger la meteo pour une ville donnee en France"""

	def __init__(self, city):
		super(WeatherDownloader, self).__init__()
		self.url = 'http://api.openweathermap.org/data/2.5/weather'
		self.params = {'q': city + ',fr', 'units': 'metric', 'lang':'fr'}

	def getCurrentWeatherData(self):
		r = requests.get(self.url, params=self.params)	
		if r.status_code == requests.codes.ok:
			data = json.loads(r.text)
			parsed_data = self.parseCurrentWeatherData(data)
			return parsed_data
		else:	
			print('Bad request')
    
    def getForecastWeatherData(self):
        r = requests.get
        #TODO

	def parseCurrentWeatherData(self, data):
		location = data['name']
		description = data['weather'][0]['description']
		temperature = data['main']['temp']
		min_temp = data['main']['temp_min']
		max_temp = data['main']['temp_max']
		humidity = data['main']['humidity']
		sunrise = data['sys']['sunrise']
		sunset = data['sys']['sunset']
		wind_speed = data['wind']['speed']
		return WeatherData ( location, description, temperature, min_temp, max_temp, sunrise, sunset, humidity, wind_speed )

	
class WeatherData(object):
	"""docstring for WeatherData"""
	def __init__(self, location, description, current_temp, min_temp, max_temp, sunrise, sunset, humidity, wind_speed ):
		super(WeatherData, self).__init__()
		self.location = location.encode('utf-8')
		self.description = description.encode('utf-8')
		self.current_temp = current_temp
		self.min_temp = min_temp
		self.max_temp = max_temp
		self.sunrise = sunrise
		self.sunset = sunset
		self.humidity = humidity
		self.wind_speed = wind_speed

	def __str__(self):
		return "Ville: {0} Temperature: {1} Description: {2} ".format(self.location, self.current_temp, self.description)
		
