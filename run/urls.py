from django.conf.urls import url

urlpatterns = [
    url(r'^run/$', 'run.views.run', name='run'),
]
