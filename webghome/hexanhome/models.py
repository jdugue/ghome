from django.db import models

class Capteur(models.Model):
	"""Classe permettant de representer un Capteur"""
	nom = models.CharField(max_length=200)

class Actionneur(models.Model):
	"""Classe permettant de representer un Actionneur"""
	nom = models.CharField(max_length=200)