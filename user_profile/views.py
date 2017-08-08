from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from .utils import user_to_json


@login_required
def profile(request):
    user_info = user_to_json(request.user)
    context = {
        "user_info": user_info
    }
    return render(request, 'mgmt.html', context)
