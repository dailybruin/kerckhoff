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

    # TODO: Add optional section - A&E / Sports / Photo / etc.

    # The slug is a short string uniquely idenitfying ALL pages
    # it is just an Id
    slug = models.SlugField(max_length=64, primary_key=True)
    page_type = models.CharField(
        max_length=2,
        choices=PAGE_TYPE_CHOICES,
        default=ONE_SHOT_PAGE,
    )
    contributors = models.ManyToManyField(User)
    is_public = models.BooleanField(db_index=True)
    public_publish_date = models.DateField(db_index=True, auto_now=True)
    title = models.CharField(max_length=128)
    series = models.ForeignKey('Series', on_delete=models.PROTECT, null=True)
    last_modified_by = models.DateField(auto_now=True)
    created_on = models.DateField(auto_now_add=True)

    @property
    def year(self):
        return self.public_publish_date.year

    @property
    def url_path(self):
        return ""

    @classmethod
    def create(cls, title, contributers, page_type=ONE_SHOT_PAGE, is_public=True, series=None, slug=None):
        if page_type == cls.SERIES_PAGE and series is None:
            raise ValueError("Series cannot be none when page is a part of a series!")

        if slug is None:
            slug = title.lower().split(" ").join("-")

        if page_type == SERIES_PAGE:
            url_path += series.slug
        elif page_type == ONE_SHOT_PAGE:
            url_path += slug
        else:
            raise ValueError("Page type of '%s' is undefined!" % page_type)
        

class Release(models.Model):
    associated_page = models.ForeignKey(
        'Page', on_delete=models.CASCADE)
    feature_img = models.ImageField(upload_to=feature_img_url, null=True)
    hash_str = models.CharField(max_length=48)
    created_on = models.DateTimeField(auto_now_add=True, db_index=True)

    @property
    def s3_prefix(self):
        """
        This helper method returns the S3 prefix for this release
        """
        return 
