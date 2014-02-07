# coding=UTF-8

from django.db import models
from django.contrib.auth.models import User

#Class for user registration
class UserProfile(models.Model):
	# This line is required. Links UserProfile to a User model instance.
	user = models.OneToOneField(User)

	# The additional attributes we wish to include.
	website = models.URLField(blank=True)
	# Install PIL before uncomment this line
	# picture = models.ImageField(upload_to='profile_images', blank=True)

	# Override the __unicode__() method to return out something meaningful!
	def __unicode__(self):
		return self.user.username

#TODO
class Profil_activation(models.Model):
	"""a définir"""
	id = models.AutoField(primary_key=True)
	nom = models.CharField(max_length=200)	
	def __unicode__(self):
		return unicode(self.nom)		

class Profil(models.Model):
	"""CLasse pour les profils définit par l'utilisateurs"""
	id = models.AutoField(primary_key=True)
	nom = models.CharField(max_length=200)	
	etat = models.BooleanField()
	def __unicode__(self):
		return unicode(self.nom)

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
	user = models.ForeignKey(User)
	def __unicode__(self):
		return unicode(self.nom)	

class Capteur(models.Model):
	"""Classe permettant de representer un Capteur"""
	id = models.AutoField(primary_key=True)
	nom = models.CharField(max_length=200 , blank=True)
	#foreign key vers les pieces
	user = models.ForeignKey(User)
	id_piece = models.ForeignKey(Piece,null = True, blank = True)
	identifiant = models.IntegerField()
	typeCapteur_CHOICES = (
		('D','détecteur de présence et de luminosité'),
		('F','Contact de fenêtre'),
		('C','Capteur température')	
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
	#foreign key vers les type
	valeur = models.BooleanField(default =False)
	user = models.ForeignKey(User)
	identifiant = models.IntegerField()
	def __unicode__(self):
		return unicode(self.nom)

class Profil_Act(models.Model):
	"""Modalité d'activation pour un profil"""
	id = models.AutoField(primary_key=True)
	id_act = models.ForeignKey(Actionneur)
	id_profil = models.ForeignKey(Profil)
	nouvelle_val = models.IntegerField()
	def __unicode__(self):
		return unicode(self.id_act)

# class Users(models.Model):
# 	"""Classe permettant de representer un Actionneur"""
# 	nom = models.CharField(max_length=200)

class Attribut(models.Model):
	"""Pour si un capteur renvoie plusieurs type de valeurs"""
	id = models.AutoField(primary_key=True)
	nom = models.CharField(max_length=200)
	valeur = models.IntegerField(blank = True,null = True)
	#foreign key vers les type
	id_type = models.ForeignKey(Type)
	identifiant = models.IntegerField()
	def __unicode__(self):
		return unicode(self.nom)

class Attr_Capteur(models.Model):
	"""Pour si un capteur renvoie plusieurs type de valeurs"""
	id = models.AutoField(primary_key=True)
	#foreign key vers les type
	id_type = models.ForeignKey(Type)
	#foreign key vers les capteurs
	id_capt = models.ForeignKey(Capteur)
	#foreign key vers les Attributs
	id_attr = models.ForeignKey(Attribut)
	def __unicode__(self):
		return unicode(self.id_capt)