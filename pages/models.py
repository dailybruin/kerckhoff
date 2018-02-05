from django.db import models
from django.contrib.auth.models import User

from .utils import feature_img_url, upload_file_url


class Series(models.Model):
    slug = models.SlugField(max_length=64, primary_key=True)
    title = models.CharField(max_length=128)
    is_public = models.BooleanField(db_index=True)


class Page(models.Model):
    ONE_SHOT_PAGE = 'OS'
    SERIES_PAGE = 'SP'
    PAGE_TYPE_CHOICES = (
        (ONE_SHOT_PAGE, 'One-shot Page'),
        (SERIES_PAGE, 'Series Page')
    )

    slug = models.SlugField(max_length=64, primary_key=True)
    page_type = models.CharField(
        max_length=2,
        choices=PAGE_TYPE_CHOICES,
        default=ONE_SHOT_PAGE,
    )
    contributors = models.ManyToManyField(User)
    is_public = models.BooleanField(db_index=True)
    public_publish_date = models.DateField(db_index=True, auto_now=True)
    #current_release = models.ForeignKey('Release', on_delete=models.PROTECT, null=True)
    title = models.CharField(max_length=128)
    series = models.ForeignKey('Series', on_delete=models.PROTECT, null=True)

    last_modified_by = models.DateField(auto_now=True)
    created_on = models.DateField(auto_now_add=True)

    @property
    def year(self):
        return self.public_publish_date.year


class Release(models.Model):
    associated_page = models.ForeignKey(
        'Page', on_delete=models.CASCADE)
    feature_img = models.ImageField(upload_to=feature_img_url, null=True)
    uploaded_files = models.FileField(upload_to=upload_file_url)

    created_on = models.DateTimeField(auto_now_add=True, db_index=True)
