from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.core import serializers
from django.views.decorators.http import require_http_methods, require_GET, require_POST
from django.core.paginator import Paginator
from django.forms.models import model_to_dict
from django.core.paginator import Paginator
from django.core.exceptions import ValidationError
import json
from .models import Package, PackageSet
from .forms import PackageForm

@require_http_methods(['GET', 'POST'])
def list_or_create(request, pset_slug):
    if request.method == 'GET':
        # List objects
        page_num = request.GET.get("page", 1)
        packages = Package.objects.filter(package_set__slug=pset_slug).all()
        paginator = Paginator(packages, 30)
        page = paginator.get_page(page_num)
        meta = {
            "total": paginator.count,
            "num_pages": paginator.num_pages,
            "current_page": page_num
        }
        if request.GET.get("endpoints"):
            results = [ model.as_endpoints() for model in page ]
        else:
            results = [ model.as_dict() for model in page]
        return JsonResponse({
            "meta": meta,
            "data": results
        })
    elif request.method == 'POST':
        # Create object
        data = json.loads(request.body)
        form_data = PackageForm(data)
        if form_data.is_valid():
            model_instance = form_data.save(commit=False)
            print(model_instance)
            try:
                m = model_instance.setup_and_save(request.user, pset_slug)
            except ValidationError as e:
                return JsonResponse(e.message_dict, status=400)
            return JsonResponse(model_to_dict(m), status=201)
        else:
            return JsonResponse(form_data.errors, status=400)
        # Do more processing
        # return HttpResponse(status=201)

@require_GET
def list_psets(request):
    res = PackageSet.objects.all()
    results = [ model.as_dict() for model in res]
    return JsonResponse({"data": results})

@require_GET
def show_one(request, pset_slug, id):
    package = Package.objects.get(package_set__slug=pset_slug, slug=id)
    return JsonResponse(model_to_dict(package))


@require_POST
def update_package(request, pset_slug, id):
    package = Package.objects.get(package_set__slug=pset_slug, slug=id)
    res = package.fetch_from_gdrive(request.user)
    return JsonResponse(model_to_dict(res))