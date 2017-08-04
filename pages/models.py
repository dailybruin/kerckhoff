from django.db import models
from django.contrib.auth.models import User


class Series(models.Model):
    slug = models.SlugField(max_length=64, primary_key=True)
    title = models.CharField(max_length=128)
    is_public = models.BooleanField(db_index=True)


class Page(models.Model):
    slug = models.SlugField(max_length=64, primary_key=True)
    contributors = models.ManyToManyField(User)
    is_public = models.BooleanField(db_index=True)
    public_publish_date = models.DateField(db_index=True, auto_now=True)
    current_release = models.OneToOneField('Release', on_delete=models.PROTECT)

    last_modified_by = models.DateField(auto_now=True)
    created_on = models.DateField(auto_now_add=True)

    @property
    def year(self):
        return self.public_publish_date.year

    class Meta:
        abstract = True


class OneShotPage(Page):
    title = models.CharField(max_length=128)


class SeriesPage(Page):
    series = models.ForeignKey('Series', on_delete=models.PROTECT)

    @property
    def title(self):
        return "{0} {1}".format(self.series.title, self.year)


class Release(models.Model):
    page = models.ForeignKey(
        'Page', on_delete=models.CASCADE)
    feature_img = models.ImageField(upload_to=feature_img_url, null=True)
    uploaded_files = models.FileField(upload_to=upload_file_url)

    created_on = models.DateTimeField(auto_now_add=True, db_index=True)


# Utils

def feature_img_url(instance, filename):
    return "{0}/{1}/img/{2}".format(instance.page.slug, instance.created_on.timestamp(), filename)


def upload_file_url(instance, filename):
    return "{0}/{1}/files/{2}".format(instance.page.slug, instance.created_on.timestamp(), filename)
