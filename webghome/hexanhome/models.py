from django.db import models

class Capteur(models.Model):
	"""Classe permettant de representer un Capteur"""
	nom = models.CharField(max_length=200)