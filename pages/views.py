from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import json
from django.http import HttpResponse
from pages.models import Page
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import math

# Create your views here.

def index(request):
    return render(request, 'index.html')

def pages(request):
    #uses params to get pages
    pagesPerQuery = int(request.GET['pagesPerQuery'])
    queryNumber = int(request.GET['queryNumber'])
    paginator = Paginator(Page.objects.all(), pagesPerQuery, allow_empty_first_page=True)
    currentQuery = paginator.get_page(queryNumber)

    #adds each page's data to dict
    data = {}
    for page in currentQuery:
        eachPageData = {}
        eachPageData["Title"] = page.title
        eachPageData["Page Type"] = page.page_type
        eachPageData["Public"] = page.is_public
        data[page.slug] = eachPageData;

    #converts data to JSON and returns
    pageJSON = json.dumps(data)
    return HttpResponse(pageJSON, content_type='application/json')
