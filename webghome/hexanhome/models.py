from django.db import models

#TODO
class Profil_activation(models.Model):
	"""a définir"""
	nom = models.CharField(max_length=200)			

class Profil(models.Model):
	"""CLasse pour les profils définit par l'utilisateurs"""
	nom = models.CharField(max_length=200)	
	etat = BooleanField()

class Profil_Act(models.Model):
	"""Modalité d'activation pour un profil"""
	id_act = ForeignKey(Actionneur)
	id_profil = ForeignKey(Profil)
	nouvelle_val = IntegerField() 

class Piece(models.Model):
	"""Piece dans laquelle se trouve le Capteur/Actionneur"""
	nom = models.CharField(max_length=200)		

class Capteur(models.Model):
	"""Classe permettant de representer un Capteur"""
	nom = models.CharField(max_length=200)
	#foreign key vers les pieces
	id_piece = models.ForeignKey(Piece)

class Actionneur(models.Model):
	"""Classe permettant de representer un Actionneur"""
	nom = models.CharField(max_length=200)
	#foreign key vers les pieces
	id_piece = models.ForeignKey(Piece)
	#foreign key vers les type
	id_type = models.ForeignKey(Type)
	#0 ou 1 pour éteint ou allumé
	valeur = models.BooleanField()

class Type(models.Model):
	"""le type de la valeur renvoyé par le capteur : temperateur, allumé/éteint, etc ..."""
	nom = models.CharField(max_length=200)		

# class Users(models.Model):
# 	"""Classe permettant de representer un Actionneur"""
# 	nom = models.CharField(max_length=200)

class Attr_Capteur(models.Model):
	"""Pour si un capteur renvoie plusieurs type de valeurs"""
	#foreign key vers les type
	id_type = models.ForeignKey(Type)
	#foreign key vers les capteurs
	id_capt = models.ForeignKey(Capteur)
	#foreign key vers les Attributs
	id_attr = models.ForeignKey(Type)

class Attribut(models.Model):
	"""Pour si un capteur renvoie plusieurs type de valeurs"""
	nom = models.CharField(max_length=200)
	valeur = models.IntegerField()
	#foreign key vers les type
	id_type = models.ForeignKey(Type)