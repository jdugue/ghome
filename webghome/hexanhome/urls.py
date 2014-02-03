from django.conf.urls import patterns, url

urlpatterns = patterns('hexanhome.views',
	url(r'^$', 'index'),
    url(r'^home/$', 'home'),
    url(r'^signup/$', 'signup'),
    url(r'^profil/$', 'profil'),
    url(r'^profil/piece/(?P<piece_name_url>\w+)/$', 'piece'),
    url(r'^config/$','config'),
    url(r'^config/AjoutPiece/$','AjoutPiece'), 
    url(r'^config/AjoutActionneur2/$','AjoutActionneur2'), 
    url(r'^config/AjoutCapteur/$','AjoutCapteur'), 	
    url(r'^login/$', 'login_view'),
    url(r'^logout/$', 'logout_view'),
    url(r'^register/$','register'),
)