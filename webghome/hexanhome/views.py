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

@login_required
def home(request):
	list_capteurs = Capteur.objects.all()
	list_users = User.objects.all()

	return render_to_response('hexanhome/home.html', { 'list_capteurs': list_capteurs })
