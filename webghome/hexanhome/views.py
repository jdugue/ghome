#-*- coding: utf-8 -*-

from django.shortcuts import render; render_to_response
from hexanhome.models import *

# Create your views here.
def home(request):
	list_capteurs = Capteur.objects.all()

	return render_to_response('hexanhome/home.html', { 'list_capteurs': list_capteurs })