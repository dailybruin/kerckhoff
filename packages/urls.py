from django.conf.urls import url
from django.urls import path

from . import views

urlpatterns = [
    path('', views.list_or_create, name='list_or_create'),
    path('<str:id>/fetch', views.update_package, name='package_update'),
    path('<str:id>/', views.show_one, name='get')
]
