#-*- coding: utf-8 -*-

from django.views.generic import TemplateView

from django.http import HttpResponse, Http404, HttpResponseRedirect

from django.contrib.auth import logout
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.forms import *

from django.template import RequestContext

from django.shortcuts import *

from registration.forms import RegistrationForm
from registration.models import RegistrationProfile
# from registration.backends.default import DefaultBackend

from hexanhome.models import *
from hexanhome.forms import *
from django.core.context_processors import csrf


def index(request):
    # template = loader.get_template('hexanhome/index.html')
    return render(request , 'hexanhome/index.html')

def login(request):
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user = auth.authenticate(username=username, password=password)
    if user is not None and user.is_active:
        # Correct password, and the user is marked "active"
        auth.login(request, user)
        # Redirect to a success page.
        return HttpResponseRedirect("/home")
    else:
        # Show an error page
        return HttpResponseRedirect("/login")

    # return render_to_response('home.html', RequestContext(request))

def logout_view(request):
    logout(request)
    # Redirect to a success page.
    return HttpResponseRedirect("/account/loggedout/")

def nouvel_utilisateur(request):
    if request.POST:
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        new_user = User.objects.create_user(username=username, password=password)   
        new_user.save()
        return Redirect()
    else:
        form = RegistrationForm()
        return render_to_response('hexanhome/nouvel_utilisateur.html' , {'form':form})

def profil(request):
	context = RequestContext(request)
	piece_list = Piece.objects.all()
	context_dixt={'pieces':piece_list}
	return render_to_response('hexanhome/profil.html',context_dixt,context)

def config(request):
    return render_to_response('hexanhome/config.html', RequestContext(request))

def AjoutPiece(request):
	context = RequestContext(request)
	if request.method =='POST':
		form = PieceForm(request.POST)
		if form.is_valid():
			form.save(commit=True)
			piece_list = Piece.objects.all()
			context_dixt={'pieces':piece_list}
			return render_to_response('hexanhome/profil.html',context_dixt,context)
		else:
			return render_to_response('hexanhome/AjoutPiece.html', { 'form' : form},context)
	else :
		form = PieceForm()
		return render_to_response('hexanhome/AjoutPiece.html', { 'form' : form},context)


def AjoutActionneur(request):
	context = RequestContext(request)
	if request.method =='POST':
		form = ActionneurForm(request.POST)
		if form.is_valid():
			form.save(commit=True)
			return HttpResponseRedirect('/profil.html')
		else:
			return render_to_response('hexanhome/AjoutActionneur.html', { 'form' : form},context)
	else :
		form = ActionneurForm()
		return render_to_response('hexanhome/AjoutActionneur.html', { 'form' : form},context)

def AjoutActionneur2(request):
	c = {}
   	c.update(csrf(request))
   	context = RequestContext(request)
	if request.method =='POST':
		piece_name = request.POST['nomPiece']
		type_name = request.POST['nomType']
		nomactionneur = request.POST['NomActionneur']
		typeselect = Type.objects.get(nom =type_name)
		piece = Piece.objects.get(nom=piece_name)
		actionneur = Actionneur(nom = nomactionneur, id_piece = piece,id_type = typeselect,valeur=0)
		actionneur.save()
		url = '/profil/piece/' + piece_name +'/'
		return HttpResponseRedirect(url)
	else :
		piece_list = Piece.objects.all()
		context_dixt={'pieces':piece_list}
		type_list= Type.objects.all()
		context_dixt['types'] = type_list	
		return render_to_response('hexanhome/AjoutActionneur2.html',context_dixt,context)

def AjoutCapteur(request):
	c = {}
   	c.update(csrf(request))
   	context = RequestContext(request)
   	if request.method =='POST':
		piece_name = request.POST['nomPiece']
		nomcapteur = request.POST['NomCapteur']
		piece = Piece.objects.get(nom=piece_name)
		capteur = Capteur(nom = nomcapteur, id_piece = piece)
		capteur.save()
		piece_list = Piece.objects.all()
		context_dixt={'pieces':piece_list}
		url = '/profil/piece/' + piece_name +'/'
		return HttpResponseRedirect(url)
	else :
		piece_list = Piece.objects.all()
		context_dixt={'pieces':piece_list}
		return render_to_response('hexanhome/AjoutCapteur.html',context_dixt,context)

def piece(request, piece_name_url):
	#permet l'utilisation de la méthode POST
	c = {}
   	c.update(csrf(request))
   	context = RequestContext(request)
   	#Change un underscore de l'url par un espace
   	piece_name = piece_name_url.replace('_',' ')
   	if request.method =='POST':
   		if 'deleteroombutton' in request.POST:
			piece = Piece.objects.get(nom=piece_name)
			piece.delete()	
			return HttpResponseRedirect('/profil/')
		else : 
			return HttpResponseRedirect('/profil/')
	else :	
		#Creer un dictionnaire qui contient tout les pieces
		context_dixt={'piece_name':piece_name}
		try:
			#Verifie qu'il existe une piece avec ce nom
			piece = Piece.objects.get(nom=piece_name)
			#On ajoute la categorie objet de la base de donnée au context
			context_dixt['piece'] = piece
			list_capteurs = Capteur.objects.filter(id_piece = piece.id)
			list_actionneur = Actionneur.objects.filter(id_piece=piece.id)
			context_dixt['capteur'] = list_capteurs
			context_dixt['actionneur'] = list_actionneur
		except Piece.DoesNotExist:
			pass
		except Capteur.DoesNotExist:
			return render_to_response('hexanhome/piece.html',context_dixt, context)
		except Actionneur.DoesNotExist:
			return render_to_response('hexanhome/piece.html',context_dixt, context)

		return render_to_response('hexanhome/piece.html',context_dixt, context)

def home(request):
    list_capteurs = Capteur.objects.all()
    dump =  deep_dump_instance(list_capteurs[0])
    return render_to_response('hexanhome/home.html', { 'list_capteurs': list_capteurs, 'dump': dump })
