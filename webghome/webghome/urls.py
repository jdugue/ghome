from django.conf.urls import patterns, include, url

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
)