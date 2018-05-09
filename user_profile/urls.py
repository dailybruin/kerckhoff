from django.conf.urls import url
from django.views.generic.base import RedirectView

from . import views

#the URL to login through Google
GOOGLE_LOGIN_URL = '/accounts/google/login/?process=login&next=%%2Fmanage%%2F/'

urlpatterns = [
    url(r'^profile/$', views.profile, name='profile'),
    #redirects user to Google login page
    url(r'^login/$', RedirectView.as_view(url=GOOGLE_LOGIN_URL)),
]
