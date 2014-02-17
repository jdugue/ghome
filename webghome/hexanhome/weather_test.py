import weather
a = weather.WeatherDownloader('Lyon')
b = a.getCurrentWeatherData()
print(b.weather_condition)