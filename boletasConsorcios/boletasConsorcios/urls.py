# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from boletas.views import *
from .views import login,logout,volverHome



admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),    
    url(r'^', include('boletas.urls')),    
    url(r'^login/$', login),
    url(r'^logout/$', logout),

)+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if settings.DEBUG is False:   #if DEBUG is True it will be served automatically
    urlpatterns += patterns('',
    		url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT,}),
            url(r'^staticfiles/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
    )

handler500 = volverHome
handler404 = volverHome