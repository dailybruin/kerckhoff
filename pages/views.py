from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import json
from django.http import HttpResponse
from pages.models import Page
import math

# Create your views here.

def index(request):
    return render(request, 'index.html')

def pages(request):
    #gets list of pages
    pageList = list(Page.objects.all())

    #if queryNumber is too big, reduces it to largest possible value
    pagesPerQuery = int(request.GET['pagesPerQuery'])
    queryNumber = int(request.GET['queryNumber'])
    if pagesPerQuery*(queryNumber-1) > len(pageList):
        queryNumber = math.floor(len(pageList)/pagesPerQuery) + 1

    #assigns starting and ending indexes for pageList based on queryNumber
    start = pagesPerQuery * (queryNumber - 1)
    end = start + pagesPerQuery - 1
    end = min(end, len(pageList)-1)

    #adds each page's data to dict
    data = {}
    for i in range(start, end+1):
        eachPageData = {}
        eachPageData["Title"] = pageList[i].title
        eachPageData["Page Type"] = pageList[i].page_type
        eachPageData["Public"] = pageList[i].is_public
        data[pageList[i].slug] = eachPageData;

    #converts data to JSON and returns
    pageJSON = json.dumps(data)
    return HttpResponse(pageJSON, content_type='application/json')
