from django.conf.urls import url

from run import views

urlpatterns = [
    url(r'^run/$', views.run, name='run'),
]
