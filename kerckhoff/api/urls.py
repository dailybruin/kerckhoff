from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^sign-s3$', views.sign_s3, name='sign_s3'),
    #url('^get_aws_v4_signature/', generate_aws_v4_signature, name='s3direct-signing'),
]