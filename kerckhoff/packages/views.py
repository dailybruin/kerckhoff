import json
import math

from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.core.exceptions import ValidationError
#from django.core.paginator import Paginator
from django.forms.models import model_to_dict
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_GET, require_http_methods, require_POST
from elasticsearch_dsl import Q, Search
from elasticsearch_dsl.search import Response

from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from kerckhoff.exceptions import UserError
from kerckhoff.util.decorators import api_login_required
from search.indexes import PackageIndex
from search.search import elasticsearch_client

from .paginator import Paginator
from .forms import PackageForm
from .models import Package, PackageSet, PackageVersion
from .serializers import PackageSetSerializer, PackageSerializer, PackageVersionSerializer

class PackageSetViewSet(viewsets.ModelViewSet):
    queryset = PackageSet.objects.all().order_by("-slug")
    serializer_class = PackageSetSerializer

class PackageViewSet(viewsets.ModelViewSet):
    queryset = Package.objects.all().order_by("-updated_at")
    serializer_class = PackageSerializer

    # Just do update_package, but first do nested-url so we can fetch id
    # AND pset_slug. (id is pk aka primarykey)

    # DRF extra action 1
    # @require_POST
    # @api_login_required()
    # def update_package(request, pset_slug, id):
    #     package = Package.objects.get(package_set__slug=pset_slug, slug=id)
    #     res = package.fetch_from_gdrive(request.user)
    #     return JsonResponse(model_to_dict(res))
    @action(detail=True, methods=['post'])
    def update_package(self, request, pset_slug, id):
        package = queryset.filter(package_set__slug=pset_slug, slug=id)
        serializer = serializer_class(data=request.data)
        if serializer.is_valid():
            res = package.fetch_from_gdrive(request.user)
            return Response(model_to_dict(res))
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
        
    # DRF extra action 2
    # @require_POST
    # @api_login_required()
    # def push_to_live(request: HttpRequest, pset_slug: str, id: str):
    #     package = Package.objects.get(package_set__slug=pset_slug, slug=id)
    #     res = package.push_to_live()
    #     if res:
    #         return HttpResponse(status=200)
    #     return HttpResponse(status=400)
    @action(detail=True, methods=['post'])
    def push_to_live(self, request: HttpRequest, pset_slug: str, id: str):
        package = queryset.filter(package_set__slug=pset_slug, slug=id)
        serializer = serializer_class(data=request.data)
        if serializer.is_valid():
            res = package.push_to_live()
            if res:
                return Response({'status': 'push_to_live() ok'},
                                status=status.HTTP_200_OK)
            else:
                return Response({'status': 'push_to_live() bad request'},
                                status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

class PackageVersionViewSet(viewsets.ModelViewSet):
    queryset = PackageVersion.objects.all().order_by("-updated_at")
    serializer_class = PackageVersionSerializer
    #TODO Overwrite default drf create method, custom user input when we create a new PV instance
    

@require_http_methods(["GET", "POST"])
@api_login_required()
def list_or_create(request: HttpRequest, pset_slug: str) -> JsonResponse:
    """
    GET: List the packages for a particular PackageSet
    POST: Create a new package within the specified PackageSet
    
    Arguments:
        request {HttpRequest} -- the request
        pset_slug {str} -- the package slug ID
    
    Returns:
        JsonResponse -- a JSON of the results
    """

    if request.method == "GET":
        # List objects
        packages = (
            Package.objects.filter(package_set__slug=pset_slug)
            .order_by("-publish_date")
            .all()
        )
        paginator = Paginator(packages, 30)
        page_num = 1
        all_docs = False
        try:
            page_num = int(request.GET.get("page", 1))
            all_docs = request.GET.get("all", False)
        except ValueError as ex:
            raise UserError(str(ex))

        if not all_docs:
            page = paginator.get_page(page_num)
        else:
            page = packages

        meta = {
            "total": paginator.count,
            "num_pages": paginator.num_pages,
            "current_page": page_num,
        }
        if request.GET.get("endpoints"):
            results = [model.as_endpoints() for model in page]
        else:
            results = [model.as_dict() for model in page]
        return JsonResponse({"meta": meta, "data": results})
    elif request.method == "POST":
        # Create object
        data = json.loads(request.body)
        form_data = PackageForm(data)
        # TODO: Refactor this to have the exception automatically thrown and
        # serialized by the custom Kerckhoff exception class instead
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
    results = [model.as_dict() for model in res]
    return JsonResponse({"data": results})


@require_GET
def show_one(request, pset_slug, id):
    package = Package.objects.get(package_set__slug=pset_slug, slug=id)
    return JsonResponse(model_to_dict(package))


@require_POST
@api_login_required()
def update_package(request, pset_slug, id):
    package = Package.objects.get(package_set__slug=pset_slug, slug=id)
    res = package.fetch_from_gdrive(request.user)
    return JsonResponse(model_to_dict(res))


@require_POST
@api_login_required()
def push_to_live(request: HttpRequest, pset_slug: str, id: str):
    package = Package.objects.get(package_set__slug=pset_slug, slug=id)
    res = package.push_to_live()
    if res:
        return HttpResponse(status=200)
    return HttpResponse(status=400)


@require_GET
def search(request: HttpRequest, pset_slug: str) -> JsonResponse:
    # TODO: we may need to distinguish internal vs external search queries at some point
    query_term = request.GET.get("q", "")
    page = 1
    items_per_page = 20

    try:
        page = int(request.GET.get("page", 1))
        items_per_page = int(request.GET.get("items", 20))
    except ValueError as ex:
        raise UserError(str(ex))

    start = (page - 1) * items_per_page
    end = (page) * items_per_page

    q = Q(
        {
            "multi_match": {
                "query": query_term,
                "fields": ["article_text", "description"],
            }
        }
    )

    s = (
        Search(using=elasticsearch_client, index=PackageIndex().meta.index)
        .filter("term", package_set=pset_slug)
        .query(q)[start:end]
    )

    response: Response = s.execute().to_dict()
    return JsonResponse(
        {
            "meta": {
                "total": response["hits"]["total"],
                "current_page": page,
                "num_pages": math.ceil(
                    response["hits"]["total"] / (items_per_page + 0.0)
                ),
            },
            "data": response["hits"]["hits"],
        }
    )
