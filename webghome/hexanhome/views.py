#-*- coding: utf-8 -*-

#IMPORTS DJANGO
from django.views.generic import TemplateView

from django.http import HttpResponse, Http404, HttpResponseRedirect

from django.views.decorators.csrf import csrf_exempt

from django.contrib.auth import logout
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.forms import *

from django.template import RequestContext

from django.shortcuts import *
import requests
from thread import *

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
	logout(request)
	context = RequestContext(request)
	email = request.POST.get('email', '')
	password = request.POST.get('password', '')
	user = authenticate(email=email, password=password)
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
	else:
		if request.POST:
			return render_to_response('hexanhome/login.html', { 'erreur' : 'Erreur lors de l authentification'},context)
	return render(request,'hexanhome/login.html')
	# return render_to_response('home.html', RequestContext(request))

def logout_view(request):
	logout(request)
	# Redirect to a success page.
	return HttpResponseRedirect("/login")

@login_required(login_url='/login/')
def profil(request):
	context = RequestContext(request)
	profil_list = RuleProfile.objects.all()
	context_dixt={'profil_list':profil_list}
	return render_to_response('hexanhome/profil.html',context_dixt,context)

@login_required(login_url='/login/')
def config(request):
	piece_list = Piece.objects.filter(user= request.user)
	return render_to_response('hexanhome/config.html',{ 'piece_list' : piece_list}, RequestContext(request))

@login_required(login_url='/login/')
def AjoutPiece(request):
	context = RequestContext(request)
	if request.method =='POST':
		nompiece = request.POST['NomPiece']
		try:
			request.user.set_ip('12345')
			piece = Piece.objects.get(nom = nompiece, user = request.user)
			return render_to_response('hexanhome/AjoutPiece.html', { 'erreur' : 'Une piece de ce nom existe deja'},context)
		except Piece.DoesNotExist:
			pieceurl = nompiece.replace(' ','_')
			piece = Piece(nom = nompiece, url= pieceurl, user = request.user)
			piece.save()
			return HttpResponseRedirect('/home')
	else :
		return render_to_response('hexanhome/AjoutPiece.html',context)

@login_required(login_url='/login/')
def AjoutActionneur(request):
	c = {}
	c.update(csrf(request))
	context = RequestContext(request)
	if request.method =='POST':
		identifiant = request.POST['NumeroIdentifiant']
		try:
			actionneur = Actionneur.objects.get(identifiant = identifiant, user = request.user)
			piece_list = Piece.objects.filter(user = request.user)
			context_dixt={'pieces':piece_list}
			context_dixt['erreurID']='Un capteur avec cette ID existe deja'
			return render_to_response('hexanhome/AjoutActionneur.html',context_dixt,context)
		except:
			piece_name = request.POST['nomPiece']
			nomactionneur = request.POST['NomActionneur']
			piece = Piece.objects.get(nom=piece_name, user = request.user)
			actionneur = Actionneur(nom = nomactionneur,user=request.user, id_piece = piece,identifiant= identifiant)
			actionneur.save()
			piece_name = piece_name.replace(' ', '_')
			url = '/profil/piece/' + piece_name +'/'
			return HttpResponseRedirect(url)
	else :
			piece_list = Piece.objects.filter(user = request.user)
			if piece_list:
				context_dixt={'pieces':piece_list}
				return render_to_response('hexanhome/AjoutActionneur.html',context_dixt,context)
			else:
				return HttpResponseRedirect('/config/AjoutPiece/')

def register(request):
	context = RequestContext(request)
	if request.method == 'POST':
		user_form = CustomUserCreationForm(data=request.POST)
		if user_form.is_valid() :
			email=request.POST['email']
			password = request.POST['password1']
			CustomUser.objects.create_user(email, password)
			new_user = authenticate(email=request.POST['email'], password=request.POST['password1'])
			if new_user is not None:
				login(request, new_user)
				return HttpResponseRedirect('/home')
			else : 
				return HttpResponseRedirect('/home')
		else:
			return render_to_response('hexanhome/register.html',{'user_form': user_form,'erreur':'true'},context)

	else:
		user_form = CustomUserCreationForm()

		return render_to_response('hexanhome/register.html',{'user_form': user_form},context)

@login_required(login_url='/login/')
def AjoutCapteur(request):
	c = {}
	c.update(csrf(request))
	context = RequestContext(request)
	if request.method =='POST':
		piece_name = request.POST['nomPiece']
		nomcapteur = request.POST['NomCapteur']
		identifiant = request.POST['numeroIdentifiant']
		try:
			capteur = Capteur.objects.get(identifiant = identifiant, user = request.user )
			piece_list = Piece.objects.filter(user = request.user)
			context_dixt={'pieces':piece_list}
			context_dixt['typeCapteur_CHOICES']=Capteur.typeCapteur_CHOICES
			context_dixt['erreurID']='Un capteur avec cette ID existe deja'
			return render_to_response('hexanhome/AjoutCapteur.html',context_dixt,context)
		except Capteur.DoesNotExist:
			capteurtype = request.POST['capteurtype']
			piece = Piece.objects.get(nom=piece_name, user = request.user)
			capteur = Capteur( user = request.user,identifiant = identifiant, nom = nomcapteur, id_piece = piece, capteurtype = capteurtype )	
			capteur.save()
			try:
				type = Type.objects.get(nom = 'bool')
			except Type.DoesNotExist:
				type=None
			if(capteurtype == 'D'):
				attribut = Attribut(nom= 'presence' ,valeur=None, id_type= type , identifiant=identifiant)
				attribut.save()
				attr_capteur=Attr_Capteur(id_type=type, id_capt = capteur ,id_attr=attribut)
				attr_capteur.save()
				attribut = Attribut(nom= 'luminosite' ,valeur=None, id_type= type , identifiant=identifiant)
				attribut.save()
				attr_capteur=Attr_Capteur(id_type=type, id_capt = capteur ,id_attr=attribut)
				attr_capteur.save()
			elif(capteurtype == 'F'):
				attribut = Attribut(nom= 'contact' ,valeur=None, id_type= type , identifiant=identifiant)
				attribut.save()
				attr_capteur=Attr_Capteur(id_type=type, id_capt = capteur ,id_attr=attribut)
				attr_capteur.save()
			elif(capteurtype == 'C'):
				attribut = Attribut(nom= 'temperature' ,valeur=None, id_type= type , identifiant=identifiant)
				attribut.save()
				attr_capteur=Attr_Capteur(id_type=type, id_capt = capteur ,id_attr=attribut)
				attr_capteur.save()
			return HttpResponseRedirect('/home')
	else :
		piece_list = Piece.objects.filter(user = request.user)
		if piece_list:
			context_dixt={'pieces':piece_list}
			context_dixt['typeCapteur_CHOICES']=Capteur.typeCapteur_CHOICES
			return render_to_response('hexanhome/AjoutCapteur.html',context_dixt,context)
		else:
			return HttpResponseRedirect('/config/AjoutPiece/')

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
			piece = Piece.objects.get(nom=piece_name, user = request.user)
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
			piece = Piece.objects.get(nom=piece_name, user = request.user)
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
	if request.method =='POST':
		if'Supp_piece' in request.POST:
			piece_nom=request.POST['piece_nom']
			piece = Piece.objects.get(nom = piece_nom, user = request.user)
			piece.delete()	
			return HttpResponseRedirect('/home/')
		elif 'Supp_capteur' in request.POST:
			capteur_id=request.POST['capteur_identifiant']
			capteur = Capteur.objects.get(identifiant = capteur_id, user= request.user) 
			for capteurvalue in capteur.attr_capteur_set.all():
				capteurvalue.id_attr.delete()
				capteurvalue.delete()
			capteur.delete()
			return HttpResponseRedirect('/home/')
		elif 'Supp_actionneur' in request.POST:
			actionneur_id=request.POST['actionneur_identifiant']
			actionneur = Actionneur.objects.get(identifiant = actionneur_id, user = request.user)
			actionneur.delete()
			return HttpResponseRedirect('/home/')
		elif 'Actionner' in request.POST:
			url = request.user.ip_adress + '/actionneur'
			actionneur = Actionneur.objects.get(identifiant =request.POST['actionneur_id'], user = request.user )
			if actionneur.valeur == False:
				params = {'id_actionneur': request.POST['actionneur_id'],'action' : 'on'}
				actionneur.valeur = True
				actionneur.save()
			else:
				params = {'id_actionneur': request.POST['actionneur_id'],'action' : 'off'}
				actionneur.valeur = False
				actionneur.save()
			r = requests.get(url,params = params)
			return HttpResponseRedirect('/home/')
	else:
		w = weather.WeatherDownloader('Lyon')
		parsed = w.getCurrentWeatherData()
		return render_to_response('hexanhome/home.html', { 'weather': parsed}, context_instance=RequestContext(request))

@login_required(login_url='/login/')
def settings(request,profil_name_url):
	context = RequestContext(request)
	profil_name = profil_name_url.replace('_',' ')
	context_dixt={'profil_name' : profil_name}
	return render_to_response('hexanhome/settings.html',context_dixt,context)

def AjouterProfil(request):
	context = RequestContext(request)
	if request.method == 'POST':
		try:
			nomprofil= request.POST['NomProfil']
			profil = RuleProfile(nom=nomprofil)
			profil.save()
			profil_url = nomprofil.replace(' ','_')
			url = '/profil/settings/' + profil_url
			return HttpResponseRedirect(url)
		except:
			return render_to_response('hexanhome/AjouterProfil.html',{erreur : 'pas de nom'},context)
	else:
		listcapteur = Capteur.objects.filter(user = request.user)
		listActionneur = Actionneur.objects.filter(user = request.user)
		context_dixt={'listCapteur':listcapteur}
		context_dixt['listActionneur'] = listActionneur
		return render_to_response('hexanhome/AjouterProfil.html',context_dixt,context)

@csrf_exempt
def login_client(request):
	if request.method == 'POST':
		email = request.POST.get('email', '')
		password = request.POST.get('password', '')
		port = request.POST.get('port','')
		user = authenticate(email=email, password=password)
		if user is not None:
			ip = get_client_ip(request)
			adresse = ''.join(['http://', ip, ':', port])
			user.set_ip(adresse)
			return HttpResponse('Bien joue')
		else:
			return HttpResponse('email: ' +email+' password: '+password + '- user is none')
	return HttpResponse('email: ' +email+' password: '+password + " inconnu")
	#return HttpReponse(jsondata,mimetype='application/json')

def get_client_ip(request):
	x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
	if x_forwarded_for:
		ip = x_forwarded_for.split(',')[-1].strip()
	else:
		ip = request.META.get('REMOTE_ADDR')
	return ip

@csrf_exempt
def test_pofiles(request):
	if request.method == 'POST':
		email = request.POST.get('email', '')
		password = request.POST.get('password', '')
		user = authenticate(email=email, password=password)
		if user is not None:
			start_new_thread(test_profiles_process, )
	return HttpResponse('')

def test_profiles_process():
	profiles = RuleProfile.objects.all()
	for profile in profiles:
		profile.test_and_execute()
