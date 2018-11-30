from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from . import views

urlpatterns = [path("<str:slug>/refresh", views.PackageSetRefreshView.as_view())]

# urlpatterns = format_suffix_patterns(urlpatterns)
