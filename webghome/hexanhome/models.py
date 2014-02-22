# coding=UTF-8

from django.db import models
from django.contrib.auth.models import User
from django.utils.http import urlquote
from django.utils.translation import ugettext_lazy as _
from django.core.mail import send_mail
from django.utils import timezone
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
import home_watcher

class CustomUserManager(BaseUserManager):

	def _create_user(self, email, password,
					 is_staff, is_superuser, **extra_fields):
		"""
		Creates and saves a User with the given email and password.
		"""
		if not email:
			raise ValueError('The given email must be set')
		email = self.normalize_email(email)
		user = self.model(email=email,is_staff=is_staff, is_active=True,is_superuser=is_superuser, **extra_fields)
		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_user(self, email, password=None, **extra_fields):
		return self._create_user(email, password, False, False,
								 **extra_fields)

	def create_superuser(self, email, password, **extra_fields):
		return self._create_user(email, password, True, True,
								 **extra_fields)



class CustomUser(AbstractBaseUser, PermissionsMixin):
	"""
	A fully featured User model with admin-compliant permissions that uses
	a full-length email field as the username.

	Email and password are required. Other fields are optional.
	"""
	email = models.EmailField(_('email address'), max_length=254, unique=True)
	ip_adress = models.URLField(blank = True)
	first_name = models.CharField(_('first name'), max_length=30, blank=True)
	last_name = models.CharField(_('last name'), max_length=30, blank=True)
	is_staff = models.BooleanField(_('staff status'), default=False,
		help_text=_('Designates whether the user can log into this admin '
					'site.'))
	is_active = models.BooleanField(_('active'), default=True,
		help_text=_('Designates whether this user should be treated as '
					'active. Unselect this instead of deleting accounts.'))
	objects = CustomUserManager()

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = []

	class Meta:
		verbose_name = _('user')
		verbose_name_plural = _('users')

	def get_absolute_url(self):
		return "/users/%s/" % urlquote(self.email)

	def get_full_name(self):
		"""
		Returns the first_name plus the last_name, with a space in between.
		"""
		full_name = '%s %s' % (self.first_name, self.last_name)
		return full_name.strip()

	def get_short_name(self):
		"Returns the short name for the user."
		return self.first_name

	def get_email(self):
		return self.email

	def email_user(self, subject, message, from_email=None):
		"""
		Sends an email to this User.
		"""
		send_mail(subject, message, from_email, [self.email])

	def set_ip(self,ip):
		self.ip_adress = ip
		self.save()
		return True

class Type(models.Model):
	"""le type de la valeur renvoyé par le capteur : temperateur, allumé/éteint, etc ..."""
	id = models.AutoField(primary_key=True)
	nom = models.CharField(max_length=200)	
	def __unicode__(self):
		return unicode(self.nom)

class Piece(models.Model):
	"""Piece dans laquelle se trouve le Capteur/Actionneur"""
	id = models.AutoField(primary_key=True)
	nom = models.CharField(max_length=200)	
	url= models.CharField(max_length=200)
	user = models.ForeignKey(settings.AUTH_USER_MODEL)
	def __unicode__(self):
		return unicode(self.nom)	

class Capteur(models.Model):
	"""Classe permettant de representer un Capteur"""
	id = models.AutoField(primary_key=True)
	nom = models.CharField(max_length=200 , blank=True)
	#foreign key vers les pieces
	user = models.ForeignKey(settings.AUTH_USER_MODEL)
	id_piece = models.ForeignKey(Piece,null = True, blank = True)
	identifiant = models.CharField(max_length=8)
	typeCapteur_CHOICES = (
		('D','detecteur de presence et de luminosite'),
		('F','Contact de fenetre'),
		('C','Capteur temperature')	
	)
	capteurtype = models.CharField(max_length=1, choices=typeCapteur_CHOICES)
	def __unicode__(self):
		return unicode(self.nom)

class Actionneur(models.Model):
	"""Classe permettant de representer un Actionneur"""
	id = models.AutoField(primary_key=True)
	nom = models.CharField(max_length=200)
	#foreign key vers les pieces
	id_piece = models.ForeignKey(Piece)
	trame_on = models.CharField(max_length=28)
	trame_off = models.CharField(max_length=28)
	user = models.ForeignKey(settings.AUTH_USER_MODEL)
	identifiant = models.CharField(max_length=8)
	def __unicode__(self):
		return unicode(self.nom) 

class Attribut(models.Model):
	"""Pour si un capteur renvoie plusieurs type de valeurs"""
	id = models.AutoField(primary_key=True)
	nom = models.CharField(max_length=200)
	valeur = models.IntegerField(blank = True,null = True)
	#foreign key vers les type
	id_type = models.ForeignKey(Type,blank = True, null = True)
	identifiant = models.CharField(max_length=8)
	def __unicode__(self):
		return unicode(self.nom)

class Attr_Capteur(models.Model):
	"""Pour si un capteur renvoie plusieurs type de valeurs"""
	id = models.AutoField(primary_key=True)
	#foreign key vers les type
	id_type = models.ForeignKey(Type,blank = True, null = True)
	#foreign key vers les capteurs
	id_capt = models.ForeignKey(Capteur)
	#foreign key vers les Attributs
	id_attr = models.ForeignKey(Attribut)
	def __unicode__(self):
		return unicode(self.id_capt)


class RuleProfile(models.Model):
	"""docstring fos RuleProfile"""
	user = models.ForeignKey(settings.AUTH_USER_MODEL)
	nom = models.CharField(max_length=200)
	def __unicode__(self):
		return unicode(self.nom)

	def test_and_execute(self):
		watcher = home_watcher.HomeWatcher()
		for rule in self.presencerule_set.all():
			if not rule.is_verified(watcher.getPresence(rule.idCapteur.identifiant)):
				return False
		for rule in self.timerule_set.all():
			if not rule.is_verified(watcher.getTime()):
				return False
		for rule in self.temperaturerule_set.all():
			if not rule.is_verified(watcher.getTemperature(rule.idCapteur.identifiant)):
				return False
		for rule in self.weatherrule_set.all():
			if not rule.is_verified(watcher.getWeatherCondition()):
				return False
		for rule in self.weekdayrule_set.all():
			if not rule.is_verified(watcher.getWeekday()):
				return False

		for action in self.ruleaction_set.all():
			action.execute_action()

		return True

class RuleAction(models.Model):
	"""docstring fos RuleAction""" 
	# action doit etre 'on' ou 'off'
	action = models.CharField(max_length=200)
	profil = models.ForeignKey(RuleProfile)
	actionneur = models.ForeignKey(Actionneur)
	
	def execute_action(self):
		if action == 'on':
			action = 'on'
		elif action == 'off':
			action = 'off'
			# eteindre actionneur

class PresenceRule(models.Model):
	profil = models.ForeignKey(RuleProfile)
	isPresent = models.BooleanField(default =False)
	idCapteur = models.ForeignKey(Capteur)
	
	def is_verified(self, isPresent):
		return self.isPresent == isPresent

class TimeRule(models.Model):
	"""docstring for TimeRule"""
	profil = models.ForeignKey(RuleProfile)
	start_time = models.CharField(max_length=200)
	end_time = models.CharField(max_length=200)
	
	def is_verified(self, time):
		if self.start_time < self.end_time :
			return self.start_time < time < self.end_time
		else:
			return (self.start_time < time < 24) or (0 < time < self.end_time)

class TemperatureRule(models.Model):
	profil = models.ForeignKey(RuleProfile)
	idCapteur = models.ForeignKey(Capteur)
	temperatureValue = models.IntegerField()
	isMinimum = models.BooleanField()

	def is_verified(self, actual_temp):
		if isMinimum:
			return actual_temp < self.temperatureValue
		else:
			return actual_temp > self.temperatureValue


class WeatherRule(models.Model):
	profil = models.ForeignKey(RuleProfile)
	weatherCondition = models.CharField(max_length=200)
	"""docstring for WeatherRule"""


	def is_verified(self, weatherCondition):
		return self.weatherCondition == weatherCondition

class WeekdayRule(models.Model):
	profil = models.ForeignKey(RuleProfile)
	weekday = models.IntegerField()
	"""docstring for WeekdayRule"""


	def is_verified(self, weekDay):
		self.weekday = weekDay
		return self.weekday
