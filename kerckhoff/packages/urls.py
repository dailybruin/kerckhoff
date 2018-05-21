from django.conf.urls import url
from django.urls import path

from . import views

urlpatterns = [
    path('', views.list_psets, name='list_package_sets'),
    path('<str:pset_slug>', views.list_or_create, name='list_or_create'),
    path('<str:pset_slug>/search', views.search, name="search"),
    path('<str:pset_slug>/<str:id>/fetch', views.update_package, name='package_update'),
    path('<str:pset_slug>/<str:id>/', views.show_one, name='get'),
    path('<str:pset_slug>/<str:id>/push', views.push_to_live, name="push_to_live"),
]
