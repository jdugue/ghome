#-*- coding: utf-8 -*-

from django.views.generic import TemplateView

from django.http import HttpResponse, Http404, HttpResponseRedirect

from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from django.template import RequestContext

from django.shortcuts import *

from hexanhome.models import *

def index(request):
	# template = loader.get_template('hexanhome/index.html')
	return render(request , 'hexanhome/index.html')

def login(request):
    return render_to_response('home.html', RequestContext(request))

def logout(request):
    logout(request)
    return HttpResponseRedirect('/home')

def profil(request):
	context = RequestContext(request)
	piece_list = Piece.objects.all()
	context_dixt={'pieces':piece_list}
	return render_to_response('hexanhome/profil.html',context_dixt,context)

def piece(request, piece_name_url):
	context = RequestContext(request)
	#Change un underscore de l'url par un espace
	piece_name = piece_name_url.replace('_',' ')
	#Creer un dictionnaire qui contient tout les pieces
	context_dixt={'piece_name':piece_name}
	try:
		#Verifie qu'il existe une piece avec ce nom
		piece = Piece.objects.get(nom=piece_name)
		#On ajoute la categorie objet de la base de donnée au context
		context_dixt['piece'] = piece
	except Piece.DoesNotExist:
		pass
	return render_to_response('hexanhome/piece.html',context_dixt, context)

def home(request):
	list_capteurs = Capteur.objects.all()
	list_users = User.objects.all()

	return render_to_response('hexanhome/home.html', { 'list_capteurs': list_capteurs })
