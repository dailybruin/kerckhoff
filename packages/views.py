from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.core import serializers
from django.views.decorators.http import require_http_methods, require_GET
import json
from .models import Package
from .forms import PackageForm

@require_http_methods(['GET', 'POST'])
def list_or_create(request):
    if request.method == 'GET':
        # List objects
        packages = Package.objects.all()
        response = serializers.serialize('json', packages)
        return HttpResponse(response, content_type='application/json')
    elif request.method == 'POST':
        # Create object
        data = json.loads(request.body)
        form_data = PackageForm(data)
        if form_data.is_valid():
            model_instance = form_data.save(commit=False)
            print(model_instance)
            model_instance.setup_and_save(request.user)
            return JsonResponse(model_instance.__dict__)
        else:
            return JsonResponse(form_data.errors, status=400)
        # Do more processing
        # return HttpResponse(status=201)

@require_GET
def show_one(request, id):
    package = Package.objects.get(id=id).values()
    response = serializers.serialize('json', package)
    return HttpResponse(response, content_type='application/json')
    
    