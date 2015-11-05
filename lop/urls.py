from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'', include('landing.urls')),
    url(r'', include('run.urls')),
    url(r'', include('django_browserid.urls')),
]
