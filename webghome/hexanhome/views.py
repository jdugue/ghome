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
from django.shortcuts import redirect

from django.template import RequestContext

from django.shortcuts import *
import requests
from thread import *

# IMPORTS PERSO
from hexanhome.models import *
from hexanhome.forms import *
import weather
import actionneur_learning
from actionneur_learning import *
from django.core.context_processors import csrf
import json

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


# ID / NOM / PIECE / TRAME ON / TRAME OFF / USER / IDENTFIANT

def register(request):
	context = RequestContext(request)
	logout(request)
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
			return HttpResponseRedirect('/home')
		elif 'Supp_capteur' in request.POST:
			capteur_id=request.POST['capteur_identifiant']
			capteur = Capteur.objects.get(identifiant = capteur_id, user= request.user) 
			for capteurvalue in capteur.attr_capteur_set.all():
				capteurvalue.id_attr.delete()
				capteurvalue.delete()
			if capteur.capteurtype == 'D':
				for rules in capteur.presencerule_set.all():
					rules.profil.delete()
					rules.delete()
			if capteur.capteurtype == 'C':
				for rules in capteur.temperaturerule_set.all():
					rules.profil.delete()
					rules.delete()
			capteur.delete()
			return HttpResponseRedirect('/home')
		elif 'Supp_actionneur' in request.POST:
			actionneur_id=request.POST['actionneur_identifiant']
			actionneur = Actionneur.objects.get(identifiant = actionneur_id, user = request.user)
			for rule in actionneur.ruleaction_set.all():
				rule.profil.delete()
				rule.delete()
			actionneur.delete()
			return HttpResponseRedirect('/home')
		elif 'Actionner' in request.POST:
			actionneur = Actionneur.objects.get(id =request.POST['actionneur_id1'], user = request.user )
			sendTrameToServer([actionneur.trame_on])	
			return HttpResponseRedirect('/home')
		elif 'Eteindre' in request.POST:
			actionneur = Actionneur.objects.get(id =request.POST['actionneur_id2'], user = request.user )
			sendTrameToServer([actionneur.trame_off])	
			return HttpResponseRedirect('/home')	
		elif 'Learning' in request.POST:
			actionneur = Actionneur.objects.get(id =request.POST['actionneur_id'], user = request.user )
			url = '/config/AjoutActionneur/learning/' + str(actionneur.id)
			return HttpResponseRedirect(url)	
	else:
		w = weather.WeatherDownloader('Lyon')
		parsed = w.getCurrentWeatherData()
		return render_to_response('hexanhome/home.html', { 'weather': parsed}, context_instance=RequestContext(request))

@login_required(login_url='/login/')
def settings(request,profil_name_url):
	context = RequestContext(request)
	profil_name = profil_name_url.replace('_',' ')
	profil = RuleProfile.objects.get(user = request.user, nom = profil_name)
	context_dixt={'profil' : profil}
	if request.method == 'POST':
		if'AjouterRegle' in request.POST:
			erreur = AjouterRegle(request,profil)
			if erreur :
				context_dixt['erreurID'] = erreur
			else:
				profil_url = profil.nom.replace(' ','_')
				url = '/profil/settings/' + profil_url
				return HttpResponseRedirect(url)
		elif 'AjouterAction' in request.POST:
			AjouterAction(request,profil)
			profil_url = profil.nom.replace(' ','_')
			url = '/profil/settings/' + profil_url
			return HttpResponseRedirect(url)
		elif 'deleteprofil' in  request.POST:
			profil.delete()
			return HttpResponseRedirect('/profil')
		elif 'nombutton' in request.POST:
			nombutton = request.POST['nombutton']
			if nombutton == 'supprimerTemperatureRule':
				idrule = request.POST['idrule']
				temperaturerule = TemperatureRule.objects.get( id = idrule)
				temperaturerule.delete()
			elif nombutton == 'supprimerPresenceRule':
				idrule = request.POST['idrule']
				presencerule = PresenceRule.objects.get( id = idrule)
				presencerule.delete()
			elif nombutton == 'supprimerTimeRule':
				idrule = request.POST['idrule']
				timerule = TimeRule.objects.get( id = idrule)
				timerule.delete()
			elif nombutton == 'supprimerWeatherRule':
				idrule = request.POST['idrule']
				weatherrule = WeatherRule.objects.get( id = idrule)
				weatherrule.delete()
			elif nombutton == 'supprimerWeekRule':
				weekday = WeekdayRule.objects.filter(profil = profil)
				for rules in weekday:
					rules.delete()
			elif nombutton == 'supprimerAction':
				idrule = request.POST['idrule']
				actionrule = RuleAction.objects.get( id = idrule)
				actionrule.delete()
		listcapteurTemperature = Capteur.objects.filter(user = request.user,capteurtype = 'C')
		listcapteurPresence = Capteur.objects.filter(user = request.user,capteurtype = 'D')
		listActionneur = Actionneur.objects.filter(user = request.user)
		context_dixt['listCapteurTemperature']=listcapteurTemperature
		context_dixt['listActionneur'] = listActionneur
		context_dixt['listCapteurPresence'] = listcapteurPresence
		context_dixt['Jourcapteur_Action'] =  WeekdayRule.Jour_CHOICES
		return render_to_response('hexanhome/settings.html',context_dixt,context)				
	else:
		context_dixt={'profil' : profil}
		listcapteurTemperature = Capteur.objects.filter(user = request.user,capteurtype = 'C')
		listcapteurPresence = Capteur.objects.filter(user = request.user,capteurtype = 'D')
		listActionneur = Actionneur.objects.filter(user = request.user)
		context_dixt['listCapteurTemperature']=listcapteurTemperature
		context_dixt['listActionneur'] = listActionneur
		context_dixt['listCapteurPresence'] = listcapteurPresence
		context_dixt['Jourcapteur_Action'] =  WeekdayRule.Jour_CHOICES
		return render_to_response('hexanhome/settings.html',context_dixt,context)

@login_required(login_url='/login/')
def AjouterRegle(request, profil):
	nomDeclencheur = request.POST['nomDeclencheur']
	if nomDeclencheur == "Temperature" : 
		capteurname = request.POST['nomCapteurTemperature']
		capteur = Capteur.objects.get(user = request.user, nom = capteurname)
		temperatureValue = request.POST['temperatureValue']
		if temperatureValue == '':
			return 'Une valeur de temperature doit être donnée'
		try:
			minimum = request.POST['minimum']
			minimum=True
		except:
			minimum= False
		try:
			temperaturerule = TemperatureRule.objects.get(profil = profil,idCapteur = capteur)
			if(temperaturerule.temperatureValue != temperatureValue):
				temperaturerule.temperatureValue = temperatureValue
			if(temperaturerule.isMinimum != minimum):
				temperaturerule.isMinimum = minimum
			temperaturerule.save()
		except:
			rule = TemperatureRule(profil = profil ,idCapteur = capteur, temperatureValue = temperatureValue, isMinimum = minimum )
			rule.save() 
	elif nomDeclencheur == "Presence" : 
		capteurname = request.POST['nomCapteurPresence']
		capteur = Capteur.objects.get(user = request.user, nom = capteurname)
		try:
			present = request.POST['isPresent']
			present=True
		except:
			present= False
		try:
			presencerule = PresenceRule.objects.get(profil = profil,idCapteur =capteur)
			if presencerule.isPresent != present:
				presencerule.isPresent = present
				presencerule.save()
		except:
			presencerule = PresenceRule(profil = profil ,isPresent = present,idCapteur =capteur )
			presencerule.save()
	elif nomDeclencheur == "Jours":
		try: 
			weekday = request.POST['lundi']
			try:
				jourregle = WeekdayRule.objects.get(profil = profil, weekday = 0)
			except:
				jourregle = WeekdayRule(profil = profil, weekday = 0)
				jourregle.save()
		except:
			pass
		try:
			weekday = request.POST['mardi']
			try:
				jourregle = WeekdayRule.objects.get(profil = profil, weekday = 1)
			except:
				jourregle = WeekdayRule(profil = profil, weekday = 1)
				jourregle.save()
		except:
			pass
		try:
			weekday = request.POST['mercredi']
			try:
				jourregle = WeekdayRule.objects.get(profil = profil, weekday = 2)
			except:
				jourregle = WeekdayRule(profil = profil, weekday = 2)
				jourregle.save()
		except:
			pass
		try:
			weekday = request.POST['jeudi']
			try:
				jourregle = WeekdayRule.objects.get(profil = profil, weekday = 3)
			except:
				jourregle = WeekdayRule(profil = profil, weekday = 3)
				jourregle.save()
		except:
			pass
		try:
			weekday = request.POST['vendredi']
			try:
				jourregle = WeekdayRule.objects.get(profil = profil, weekday = 4)
			except:
				jourregle = WeekdayRule(profil = profil, weekday = 4)
				jourregle.save()
		except:
			pass
		try:
			weekday = request.POST['samedi']
			try:
				jourregle = WeekdayRule.objects.get(profil = profil, weekday = 5)
			except:
				jourregle = WeekdayRule(profil = profil, weekday = 5)
				jourregle.save()
		except:
			pass
		try:
			weekday = request.POST['dimanche']
			try:
				jourregle = WeekdayRule.objects.get(profil = profil, weekday = 6)
			except:
				jourregle = WeekdayRule(profil = profil, weekday = 6)
				jourregle.save()
		except:
			pass
	elif nomDeclencheur == "Heure":
		start_time = request.POST['heuredebut']
		end_time = request.POST['heurefin']
		timerule = TimeRule(profil = profil,start_time = start_time ,end_time= end_time)
		timerule.save()
	elif nomDeclencheur == "Meteo":
		try: 
			meteo = request.POST['thunderstorm']
			meteorule = WeatherRule(profil = profil, weatherCondition = meteo)
			meteorule.save()
		except:
			pass
		try: 
			meteo = request.POST['drizzle']
			meteorule = WeatherRule(profil = profil, weatherCondition = meteo)
			meteorule.save()
		except:
			pass
		try: 
			meteo = request.POST['rain']
			meteorule = WeatherRule(profil = profil, weatherCondition = meteo)
			meteorule.save()
		except:
			pass
		try: 
			meteo = request.POST['clouds']
			meteorule = WeatherRule(profil = profil, weatherCondition = meteo)
			meteorule.save()
		except:
			pass
		try: 
			meteo = request.POST['extreme']
			meteorule = WeatherRule(profil = profil, weatherCondition = meteo)
			meteorule.save()
		except:
			pass
	
@login_required(login_url='/login/')
def AjouterAction(request,profil):
	actionneurname = request.POST['nomActionneur']	
	action = request.POST['action']
	actionneur = Actionneur.objects.get(user = request.user , nom = actionneurname)
	try:
		action2 = RuleAction.objects.get(profil= profil, actionneur= actionneur)
		if(action2.action != action):
			action2.action = action
			action2.save()
	except:
		ruleAction = RuleAction(action = action , profil= profil, actionneur= actionneur )
		ruleAction.save()	
@login_required(login_url='/login/')
def AjouterProfil(request):
	context = RequestContext(request)
	if request.method == 'POST':
		try:
			nomprofil= request.POST['NomProfil']
			if nomprofil == '':
				context_dixt = {'erreurID':'Le champs profil ne doit pas être vide'}
			else:
				profil = RuleProfile.objects.get(user = request.user, nom = nomprofil)
				context_dixt = {'erreurID':'Un profil avec ce nom existe deja'}
			listcapteurTemperature = Capteur.objects.filter(user = request.user,capteurtype = 'C')
			listcapteurPresence = Capteur.objects.filter(user = request.user,capteurtype = 'D')
			listActionneur = Actionneur.objects.filter(user = request.user)
			context_dixt['listCapteurTemperature']=listcapteurTemperature
			context_dixt['listActionneur'] = listActionneur
			context_dixt['listCapteurPresence'] = listcapteurPresence
			context_dixt['nb_times'] = 0
			return render_to_response('hexanhome/AjouterProfil.html',context_dixt,context)
		except:
			nomprofilurl = nomprofil.replace(' ','_')
			profil = RuleProfile(nom = nomprofil, user = request.user, url= nomprofilurl)
			profil.save()
			AjouterRegle(request, profil)
			AjouterAction(request,profil)
			profil_url = profil.nom.replace(' ','_')
			url = '/profil/settings/' + profil_url
			return HttpResponseRedirect(url)	
	else:
		listcapteurTemperature = Capteur.objects.filter(user = request.user,capteurtype = 'C')
		listcapteurPresence = Capteur.objects.filter(user = request.user,capteurtype = 'D')
		listActionneur = Actionneur.objects.filter(user = request.user)
		context_dixt={'listCapteurTemperature':listcapteurTemperature}
		context_dixt['listActionneur'] = listActionneur
		context_dixt['listCapteurPresence'] = listcapteurPresence
		context_dixt['nb_times'] = 0
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

@csrf_exempt
def test_profiles(request):
	if request.method == 'POST':
		email = request.POST.get('email', '')
		password = request.POST.get('password', '')
		user = authenticate(email=email, password=password)
		if user is not None:
			start_new_thread(test_profiles_process,())
	return HttpResponse('')

def test_profiles_process():
	profiles = RuleProfile.objects.all()
	f = open('workfile.txt', 'w')
	for profile in profiles:
		f.write(profile.nom + '\n')
		if( profile.test_and_execute() ):
			f.write('Ca a marche\n')
		else:
			f.write('ca a pas marche\n')
	f.close()
@login_required(login_url='/login/')
def learning(request,actionneur_id):
	context = RequestContext(request)
	if request.method =='POST':
		actionneur_id = request.POST['actionneur_identifiant']
		actionneur = Actionneur.objects.get(user = request.user, id = actionneur_id )
		try:
			sendTrameToServer([actionneur.trame_on])
		except:
			pass
		return HttpResponseRedirect('/home')	
	else :
		actionneur = Actionneur.objects.get(user = request.user, id = actionneur_id)
		context_dixt={'actionneur':actionneur}
		return render_to_response('hexanhome/learning.html',context_dixt,context)

@login_required(login_url='/login/')
def AjoutActionneur(request):
	c = {}
	c.update(csrf(request))
	context = RequestContext(request)
	if request.method =='POST':
		piece_name = request.POST['nomPiece']
		nomactionneur = request.POST['NomActionneur']
		try : 
			piece = Piece.objects.get(nom=piece_name, user = request.user)
			actionneur = Actionneur.objects.get(nom = nomactionneur,user=request.user, id_piece = piece)
			context_dixt = {'erreurID':'Un actionneur avec cette ID existe deja'}
			piece_list = Piece.objects.filter(user = request.user)
			context_dixt['pieces']=piece_list
			return render_to_response('hexanhome/AjoutActionneur.html',context_dixt,context)
		except:
			actionneur = Actionneur(nom = nomactionneur,user=request.user, id_piece = piece)
			actionneur.save()
			actionneur.identifiant = getFictiveButtonId(actionneur.id)
			actionneur.trame_on = getTrameON(actionneur.identifiant)
			actionneur.trame_off = getTrameOFF(actionneur.identifiant)
			actionneur.save()
			piece_name = piece_name.replace(' ', '_')
			url = '/config/AjoutActionneur/learning/' + str(actionneur.id)
			return HttpResponseRedirect(url)
	else :
		piece_list = Piece.objects.filter(user = request.user)
		if piece_list:
			context_dixt={'pieces':piece_list}
			return render_to_response('hexanhome/AjoutActionneur.html',context_dixt,context)
		else:
			return HttpResponseRedirect('/config/AjoutPiece/')

@csrf_exempt
def regle(request):
	context = RequestContext(request)
	listcapteurTemperature = Capteur.objects.filter(user = request.user,capteurtype = 'C')
	listcapteurPresence = Capteur.objects.filter(user = request.user,capteurtype = 'D')
	context_dixt = {'listCapteurTemperature':listcapteurTemperature}
	context_dixt['listCapteurPresence'] = listcapteurPresence
	return render_to_response('hexanhome/AjoutRegle.html',context_dixt,context)

@csrf_exempt
def action(request):
	context = RequestContext(request)
	listActionneur = Actionneur.objects.filter(user = request.user)
	context_dixt={'listActionneur': listActionneur}
	return render_to_response('hexanhome/AjoutAction.html',context_dixt,context)

