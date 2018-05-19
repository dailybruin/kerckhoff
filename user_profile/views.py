from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
import urllib.parse

from .utils import user_to_json

GOOGLE_LOGIN_URL_PREFIX = '/accounts/google/login/?'

@login_required
def profile(request):
    user_info = user_to_json(request.user)
    context = {
        "user_info": user_info
    }
    return render(request, 'mgmt.html', context)

#the view to redirect to the Google login page
def redirectToGoogle(request):
    coming_from = request.GET.get("next", "/manage")
    url_params = {
        "process": "login",
        "next": coming_from
    }
    suffix = urllib.parse.urlencode(url_params)
    return redirect(GOOGLE_LOGIN_URL_PREFIX + suffix)
