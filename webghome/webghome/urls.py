from django.conf.urls import patterns, include, url
from hexanhome.models import Piece
from django.contrib import admin
from django.contrib.auth.views import login, logout
admin.autodiscover()

# from hexanhome.views import HomeView

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'webghome.views.home', name='home'),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('hexanhome.urls')),
    # url(r'^home/$', HomeView.as_view(), name='home'),
    # url(r'^login/$', 'django.contrib.auth.views.login'),
    # url(r'^logout/$', 'logout'),	
    (r'^login/$',  login),
    (r'^logout/$', logout),
    # url(r'^login/$', 'django.contrib.auth.views.login'),
    url(r'^logout/$', 'logout'),	
)

