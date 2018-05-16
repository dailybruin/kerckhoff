"""kerckhoff URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin

from user_profile import views as profile_views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^user/(?P<name>\w+)/$', profile_views.profile),
    url(r'^manage/', profile_views.profile),
    url(r'^accounts/', include('user_profile.urls')),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^api/', include('api.urls')),
    url(r'^api/tags/', include('tags.urls')),
    url(r'^api/packages/', include('packages.urls')),
    url(r'', include('pages.urls')),
]
