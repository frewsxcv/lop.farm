from django.conf.urls import url

urlpatterns = [
    url(r'^$', 'landing.views.landing', name='landing'),
]
