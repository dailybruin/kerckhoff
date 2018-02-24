from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.list_or_create, name='list_or_create'),
    url('/<int:id>/', views.show_one, name='get')
]
