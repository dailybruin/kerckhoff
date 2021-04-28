import re
import logging

import requests
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.postgres.fields import JSONField
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from requests_oauthlib import OAuth2Session

from search.indexes import PackageIndex

from .utils import transfer_to_s3, rewrite_image_url
from .google_drive_actions import get_file, get_oauth2_session, list_folder, create_package, add_to_repo_folder
from .constants import *

logger = logging.getLogger(settings.APP_NAME)

class PackageSet(models.Model):
    slug = models.SlugField(max_length=32, primary_key=True)
    drive_folder_id = models.CharField(max_length=512, blank=True)
    drive_folder_url = models.URLField()
    default_content_type = models.CharField(max_length=2, choices=CONTENT_TYPE_CHOICES, default=PLAIN_TEXT)

    def as_dict(self):
        return {
            "slug": self.slug,
            "gdrive_url": self.drive_folder_url,
        }

    def save(self, *args, **kwargs):
        self.drive_folder_id = self.drive_folder_url.rsplit('/', 1)[-1]
        super().save(*args, **kwargs)

    def populate(self, user):
        print("Starting populate for %s" % self.slug)
        google = get_oauth2_session(user)
        # we don't care about the aml_data dict here
        _, _, folders, _ = list_folder(google, self)
        instances = []
        for folder in folders:
            try:
                exists = Package.objects.get(slug=folder["title"])
                instances.append(exists)
            except Package.DoesNotExist:
                pkg = Package.objects.create(
                    slug=folder["title"],
                    drive_folder_id=folder["id"],
                    drive_folder_url=folder["alternateLink"],
                    publish_date=timezone.now(),
                    package_set=self
                )
                instances.append(pkg)
        for instance in instances:
            print("Processing %s" % instance.slug)
            try:
                instance.fetch_from_gdrive(user)
            except Exception as e:
                print("%s failed with error: %s" % (instance.slug, e))
                continue
    

class Package(models.Model):
    slug = models.CharField(max_length=64, primary_key=True)
    description = models.TextField(blank=True)
    drive_folder_id = models.CharField(max_length=512)
    drive_folder_url = models.URLField()
    metadata = JSONField(blank=True, default=dict, null=True)
    images = JSONField(blank=True, default=dict, null=True)
    data = JSONField(blank=True, default=dict, null=True)
    processing = models.BooleanField(default=False)
    cached_article_preview = models.TextField(blank=True)
    publish_date = models.DateField()
    last_fetched_date = models.DateTimeField(null=True, blank=True)
    package_set = models.ForeignKey(PackageSet, on_delete=models.PROTECT)
    _content_type = models.CharField(max_length=2, choices=CONTENT_TYPE_CHOICES, blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Versioning
    latest_version = models.ForeignKey('PackageVersion', related_name='versions', on_delete=models.CASCADE, null=True, blank=True)

    @property
    def content_type(self):
        if self._content_type == "":
            return self.package_set.default_content_type
        else:
            return self._content_type

    # For versioning feature, accepts string arguments name(of creator) and change_summary
    def create_version(self, user, change_summary):
        pv = PackageVersion(package=self, article_data=self.cached_article_preview, data=self.data, creator=user, version_description=change_summary)
        pv.save()
        self.latest_version = pv
        # return 'Successfully created PackageVersion object!'


    def indexing(self):
        """
        Adds to the elasticsearch index the current package instance
        """
        idx = PackageIndex(
            meta={'id': self.slug},
            slug=self.slug,
            package_set=self.package_set.slug,
            description=self.description,
            cached_article_preview=self.cached_article_preview,
            article_text=self.cached_article_preview, # TODO: Change when article versioning is completed
            publish_date=self.publish_date
        )
        idx.save()
        return idx.to_dict(include_meta=True)

    def save(self, *args, **kwargs):
        self.indexing()
        super().save(*args, **kwargs)

    def as_endpoints(self):
        return {
            "slug": self.slug,
            "endpoint": "/api/packages/" + self.package_set.slug + "/" + self.slug
        }

    def as_dict(self):
        return {
            "slug": self.slug,
            "description": self.description,
            "gdrive_url": self.drive_folder_url,
            "images": self.images,
            "data": self.data,
            "article": self.cached_article_preview,
            "publish_date": self.publish_date,
            "last_fetched_date": self.last_fetched_date
        }

    def setup_and_save(self, user, pset_slug):
        google = get_oauth2_session(user)
        if self.drive_folder_url == "":
            url, drive_id = create_package(google, self)
            self.drive_folder_id = drive_id
            self.drive_folder_url = url
        else:
            folder_id = self.drive_folder_url.rsplit('/', 1)[-1]
            details = get_file(google, folder_id)
            if details.get("mimeType") != "application/vnd.google-apps.folder":
                raise ValidationError({"drive_folder_url" : ["The Google drive link must be a link to an existing folder!"]})
            self.drive_folder_id = folder_id
            results = add_to_repo_folder(google, self)
            print(results)
        self.cached_article_preview = ""
        self.images = {}
        self.package_set = PackageSet.objects.get(slug=pset_slug)
        self.save()
        return self

    def push_to_live(self):
        res = requests.post(settings.LIVE_PUSH_SERVER + "/update", json={'id': self.package_set.slug + '/' + self.slug})
        return res.ok

    # TODO - put this in a workqueue
    def fetch_from_gdrive(self, user):
        # TODO Actually use this manual locking lol
        self.processing = True
        self.save()
        try:
            google = get_oauth2_session(user)
            text, images, _, aml_data = list_folder(google, self)
            self.cached_article_preview = text
            if self.images is None:
                self.images = {}
            self.images["gdrive"] = images
            self.data = aml_data
            transfer_to_s3(google, self)
            self.cached_article_preview = rewrite_image_url(self)
            self.last_fetched_date = timezone.now()
            # Create new PV instance
            # TODO Once frontend is done, query for proper change_summary. Default is last_fetched_date
            self.create_version(user, "New PackageVersion created on {0}".format(self.last_fetched_date))

        except Exception as e:
            raise e
        finally:
            self.processing = False
            self.save()

        return self

# Snapshot of a Package instance at a particular time
class PackageVersion(models.Model):
    package = models.ForeignKey(Package, on_delete=models.PROTECT)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    version_description = models.TextField(blank=True)
    article_data = models.TextField(blank=True)
    data = JSONField(blank=True, default=dict)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    #TODO 
    # Add package stateEnum for future (freeze should change state)