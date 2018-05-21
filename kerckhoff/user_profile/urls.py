from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^profile/$', views.profile, name='profile'),
    #redirects user to Google login page
    url(r'^login/$', views.redirectToGoogle, name="rediect_to_Google"),
]
