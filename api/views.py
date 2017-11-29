from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required

from django.conf import settings

@login_required
def get_random(request):
    x = request.GET.get('q', "world")
    return JsonResponse({"hello": x, "s3key": settings.S3_SITE_UPLOAD_BUCKET})