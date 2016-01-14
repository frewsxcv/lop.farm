from django.conf.urls import url

from run import views

urlpatterns = [
    url(r'^trigger_run/$', views.trigger_run, name='trigger_run'),
    url(r'^run/(?P<run_id>[0-9]+)/$', views.run, name='run'),
]
