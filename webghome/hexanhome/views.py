#-*- coding: utf-8 -*-

#IMPORTS DJANGO
from django.views.generic import TemplateView

from django.http import HttpResponse, Http404, HttpResponseRedirect

from django.contrib.auth import logout
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.forms import *

from django.template import RequestContext

from django.shortcuts import *

# IMPORTS AUTRES
# from registration.forms import RegistrationForm
# from registration.models import RegistrationProfile
# from registration.backends.default import DefaultBackend

# IMPORTS PERSO
from hexanhome.models import *
from hexanhome.forms import *
import weather

from django.core.context_processors import csrf

@login_required(login_url='/login/')
def index(request):
    # template = loader.get_template('hexanhome/index.html')
    return render(request , 'hexanhome/index.html')

def login_view(request):
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user = authenticate(username=username, password=password)
    if user is not None:
    	if user.is_active:
	        # Correct password, and the user is marked "active"
	        login(request, user)
	        # Redirect to a success page.
    	if request.GET.get('next', ''):
    		next = request.POST.get('next', '')
    		return HttpResponseRedirect(next)
    	else:
	        return HttpResponseRedirect("/home")
	# Show an error page
    return render(request,'hexanhome/login.html')
	# return render_to_response('home.html', RequestContext(request))

def logout_view(request):
    logout(request)
    # Redirect to a success page.
    return HttpResponseRedirect("/login")

@login_required(login_url='/login/')
def signup(request):
    if request.POST:
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        new_user = User.objects.create_user(username=username, password=password)   
        new_user.save()
        return HttpResponseRedirect("/home")
    else:
        # form = RegistrationForm()
        return render(request,'hexanhome/signup.html')

@login_required(login_url='/login/')
def profil(request):
	context = RequestContext(request)
	piece_list = Piece.objects.all()
	context_dixt={'pieces':piece_list}
	for piece in piece_list:
		piece.url = piece.nom.replace(' ', '_')
	return render_to_response('hexanhome/profil.html',context_dixt,context)

@login_required(login_url='/login/')
def config(request):
    return render_to_response('hexanhome/config.html', RequestContext(request))

@login_required(login_url='/login/')
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

@login_required(login_url='/login/')
def AjoutActionneur2(request):
	c = {}
   	c.update(csrf(request))
   	context = RequestContext(request)
	if request.method =='POST':
		piece_name = request.POST['nomPiece']
		type_name = request.POST['nomType']
		nomactionneur = request.POST['NomActionneur']
		value= request.POST['Value1']
		if(value == 'option1'):
			value=0
		else:
			value=1
		typeselect = Type.objects.get(nom =type_name)
		piece = Piece.objects.get(nom=piece_name)
		actionneur = Actionneur(nom = nomactionneur, id_piece = piece,id_type = typeselect,valeur= value)
		actionneur.save()
		piece_name = piece_name.replace(' ', '_')
		url = '/profil/piece/' + piece_name +'/'
		return HttpResponseRedirect(url)
	else :
		piece_list = Piece.objects.all()
		context_dixt={'pieces':piece_list}
		type_list= Type.objects.all()
		context_dixt['types'] = type_list	
		return render_to_response('hexanhome/AjoutActionneur2.html',context_dixt,context)

@login_required(login_url='/login/')
def AjoutCapteur(request):
	c = {}
   	c.update(csrf(request))
   	context = RequestContext(request)
   	if request.method =='POST':
		piece_name = request.POST['nomPiece']
		nomcapteur = request.POST['NomCapteur']
		identifiant = request.POST['numeroIdentifiant']
		piece = Piece.objects.get(nom=piece_name)
		capteur = Capteur( identifiant = identifiant, nom = nomcapteur, id_piece = piece)	
		capteur.save()
		piece_name = piece_name.replace(' ', '_')
		url = '/profil/piece/' + piece_name +'/'
		return HttpResponseRedirect(url)
	else :
		piece_list = Piece.objects.all()
		capteur_list = Capteur.objects.all()
		context_dixt={'pieces':piece_list}
		context_dixt['capteurs'] = capteur_list
		return render_to_response('hexanhome/AjoutCapteur.html',context_dixt,context)

@login_required(login_url='/login/')
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
		if 'NomCapteur' in request.POST:
			nouveauxnom = request.POST['NomCapteur']
			oldname = request.POST['oldname']
			Capteur.objects.filter(nom = oldname).update(nom = nouveauxnom)
			url = '/profil/piece/' + piece_name_url +'/'
			return HttpResponseRedirect(url)
		else : 
			return HttpResponseRedirect('/profil/')
	
	else :	
		#Creer un dictionnaire qui contient tout les pieces
		context_dixt={'piece_name':piece_name}
		try:
			#Verifie qu'il existe une piece avec ce nom
			piece = Piece.objects.get(nom=piece_name)
			#On ajoute la categorie objet de la base de donnée au context
			context_dixt['piece_url'] = piece_name_url
			context_dixt['piece'] = piece
			list_capteurs = Capteur.objects.filter(id_piece = piece.id)
			list_actionneur = Actionneur.objects.filter(id_piece=piece.id)
			capteur_value={}
			for capteur in list_capteurs:
				list_attribut=Attr_Capteur.objects.filter(id_capt = capteur.id)
				capteur_value[capteur] = list_attribut
			context_dixt['capteurValue']=capteur_value
			context_dixt['actionneur'] = list_actionneur
		except Piece.DoesNotExist:
			raise Http404
		except Attribut.DoesNotExist:
			pass
		except Capteur.DoesNotExist:
			return render_to_response('hexanhome/piece.html',context_dixt, context)
		except Actionneur.DoesNotExist:
			return render_to_response('hexanhome/piece.html',context_dixt, context)

		return render_to_response('hexanhome/piece.html',context_dixt, context)

@login_required(login_url='/login/')
def home(request):
    list_capteurs = Capteur.objects.all()
    w = weather.WeatherDownloader('Lyon')
    parsed = w.getCurrentWeatherData()
    return render_to_response('hexanhome/home.html', { 'list_capteurs': list_capteurs, 'weather': parsed}, context_instance=RequestContext(request))
