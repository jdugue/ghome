from django.conf.urls import patterns, url

urlpatterns = patterns('hexanhome.views',
	url(r'^$', 'index'),
    url(r'^home/$', 'home'),
    url(r'^profil/$', 'profil'),
    url(r'^profil/piece/(?P<piece_name_url>\w+)/$', 'piece'),
    url(r'^config/$','config'),
    url(r'^config/AjoutPiece/$','AjoutPiece'), 
    url(r'^config/AjoutActionneur/$','AjoutActionneur'), 
    url(r'^config/AjoutCapteur/$','AjoutCapteur'), 	
    url(r'^login/$', 'login_view'),
    url(r'^logout/$', 'logout_view'),
    url(r'^register/$','register'),
    url(r'^profil/settings/(?P<profil_name_url>\w+)/$','settings'),
    url(r'profil/Ajouter_Profil/$','AjouterProfil'),
    #URLS DE L'API
    url(r'login_client/$','login_client'),
    url(r'test_profiles/$','test_profiles'),
)