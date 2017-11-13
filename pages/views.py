from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import json
from django.http import HttpResponse
from pages.models import Page

# Create your views here.

def index(request):
    return render(request, 'index.html')

def pages(request):
    return HttpResponse(json.dumps(list(Page.objects.all())), content_type='application/json')
