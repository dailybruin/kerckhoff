from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import json
from django.http import HttpResponse

json_data = '{"hello": "world", "foo": "bar"}'
data = json.loads(json_data)

# Create your views here.


def index(request):
    return render(request, 'index.html')

def pages(request):
    return HttpResponse(json.dumps(data), content_type='application/json')
