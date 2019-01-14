from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
import urllib.parse
from kerckhoff.util.decorators import api_login_required
from django.views.decorators.http import require_http_methods, require_GET, require_POST
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
import json
from .utils import user_to_json
from .models import UserProfile
from .serializers import UserProfileSerializer

GOOGLE_LOGIN_URL_PREFIX = "/accounts/google/login/?"


@login_required
def profile(request):
    user_info = user_to_json(request.user)
    context = {"user_info": user_info}
    return render(request, "mgmt.html", context)


class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all().order_by("-last_name")
    serializer_class = UserProfileSerializer

    @action(detail=False, url_path="current", url_name="current")
    def current_user_info(self, request):
        # bad - we shouldnt convert from json to string to json
        return Response(json.loads(user_to_json(request.user)))


# the view to redirect to the Google login page
def redirect_to_google_login(request):
    coming_from = request.GET.get("next", "/manage")
    url_params = {"process": "login", "next": coming_from}
    suffix = urllib.parse.urlencode(url_params)
    return redirect(GOOGLE_LOGIN_URL_PREFIX + suffix)
