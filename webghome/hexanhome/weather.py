import requests
import requests.exceptions
import json

weather_condition = {'thunderstorm': 200, 'drizzle': 300, 'rain' : 500, 
                            'snow' : 600, 'clouds': 800, 'extreme' : 900}

class WeatherDownloader(object):
    """Classe pour telecharger la meteo pour une ville donnee en France"""

    def __init__(self, city):
        super(WeatherDownloader, self).__init__()
        self.url = 'http://api.openweathermap.org/data/2.5/weather'
        self.params = {'q': city + ',fr', 'units': 'metric', 'lang':'fr'}

    def getCurrentWeatherData(self):
        try:
            r = requests.get(self.url, params=self.params)  
            if r.status_code == requests.codes.ok:
                data = json.loads(r.text)
                parsed_data = self.parseCurrentWeatherData(data)
                return parsed_data
            else:   
                print('Bad request')
        except requests.ConnectionError:
            print('ConnectionError exception')
        except requests.HTTPError:
            print('HTTPError exception')
        except requests.Timeout:
            print('Timeout exception')
        except requests.TooManyRedirects:
            print('TooManyRedirects exception')
        parsed_data = None
        return parsed_data

    def parse_weather_condition_id(self, weather_id):
        weather_condition = None
        if 200 < weather_id <= 300:
            weather_condition = 'thunderstorm'
        elif 300 <= weather_id < 400:
            weather_condition = 'drizzle'
        elif 500 <= weather_id < 600:
            weather_condition = 'rain'
        elif 800 <= weather_id < 900:
            weather_condition = 'clouds'
        elif 900 <= weather_id < 950:
            weather_condition = 'extreme'
        return weather_condition

    def parseCurrentWeatherData(self, data):
        if data:
            location = data['name']
            description = data['weather'][0]['description']
            weather_id = data['weather'][0]['id']
            temperature = data['main']['temp']
            min_temp = data['main']['temp_min']
            max_temp = data['main']['temp_max']
            humidity = data['main']['humidity']
            sunrise = data['sys']['sunrise']
            sunset = data['sys']['sunset']
            wind_speed = data['wind']['speed']
            return WeatherData ( location, description, temperature, min_temp, max_temp, 
            sunrise, sunset, humidity, wind_speed, self.parse_weather_condition_id(weather_id))
        else:
            return WeatherData()

    
class WeatherData(object):
    """docstring for WeatherData"""
    def __init__(self, location, description, current_temp, min_temp, max_temp, sunrise, sunset, 
                                                        humidity, wind_speed, weather_condition ):
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
        self.weather_condition = weather_condition

    def __init(self):
        super(WeatherData, self).__init__()
        self.location = None
        self.description = None
        self.current_temp = None
        self.min_temp = None
        self.max_temp = None
        self.sunrise = None
        self.sunset = None
        self.humidity = None
        self.wind_speed = None
        self.weather_condition = None

    def __str__(self):
        return "Ville: {0} Temperature: {1} Description: {2} Condition: {3} ".format(self.location, self.current_temp, 
            self.description, self.weather_condition)



