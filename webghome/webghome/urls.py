from django.conf.urls import patterns, include, url
from hexanhome.models import Piece
from django.contrib import admin
admin.autodiscover()

# from hexanhome.views import HomeView

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'webghome.views.home', name='home'),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('hexanhome.urls')),	
)

