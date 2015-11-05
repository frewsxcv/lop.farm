from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'landing.views.landing'),
    url(r'^run/$', 'run.views.run'),
    url(r'', include('django_browserid.urls')),
]
