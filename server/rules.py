class RuleProfile(object):
	"""docstring fos RuleProfile"""
	def __init__(self, user):
		super(RuleProfile, self).__init__()
		self.rules = []
		self.actions = []
	
	def add_rule(self, rule):
		self.rules.append(rule)

	def add_action(self, action):
		self.actions.append(rule)

	def test_and_execute(self):



class RuleAction(object):
	"""docstring fos RuleAction""" 

	# action doit etre 'on' ou 'off'
	def __init__(self, action, actionneur_id):
		super(RuleAction, self).__init__()
		self.action = action
		self.actionneur_id

	def execute_action(self):
		if action == 'on':
			# allumer actionneur
		elif : action == 'off'
			# eteindre actionneur


class PresenceRule(object):

	def __init__(self, isPresent):
		super(PresenceRule, self).__init__()
		self.isPresent = isPresent

	def is_verified(self, isPresent):
		return self.isPresent == isPresent

class TimeRule(object):
	"""docstring for TimeRule"""
	def __init__(self, start_time, end_time):
		super(TimeRule, self).__init__()
		self.start_time = start_time
		self.end_time = end_time

	def is_verified(self, time):
		if self.start_time < self.end_time :
			return self.start_time < time < self.end_time
		else:
			return (self.start_time < time < 24) or (0 < time < self.end_time)

class TemperatureRule(object):

	def __init__(self, temperatureValue, isMinimum):
		super(TemperatureRule, self).__init__()
		self.temperatureValue = temperatureValue
		self.isMinimum = isMinimum

	def is_verified(self, temperatureValue):
		return isMinimum ? temperatureValue < self.temperatureValue :  temperatureValue > self.temperatureValue

class WeatherRule(object):
	"""docstring for WeatherRule"""
	def __init__(self, weatherCondition):
		super(WeatherRule, self).__init__()
		self.weatherCondition = weatherCondition
	
	def is_verified(self, weatherCondition):
		return self.weatherCondition == weatherCondition

class WeekdayRule(object)
	"""docstring for WeekdayRule"""
	def __init__(self, weekday):
		super(WeekdayRule, self).__init__()
		self.weekday = weekday
		
	def is_verified(self, weekDay)
		return self.weekday = weekday