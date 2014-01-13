from django.conf.urls import patterns, include, url
from hexanhome.models import Piece
from django.contrib import admin
admin.autodiscover()

# from hexanhome.views import HomeView

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'webghome.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    # url(r'^home/$', HomeView.as_view(), name='home'),
    url(r'^$', 'hexanhome.views.index'),
    url(r'^home/$', 'hexanhome.views.home'),
    url(r'^login/$', 'django.contrib.auth.views.login'),
    url(r'^logout/$', 'logout'),	
    url(r'^profil/$', 'hexanhome.views.profil'),
    url(r'^profil/piece/(?P<piece_name_url>\w+)/$', 'hexanhome.views.piece'),		

)