from django.db import models
from django.contrib.postgres.fields import JSONField, ArrayField
from django.conf import settings
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from allauth.socialaccount.models import SocialToken
from requests_oauthlib import OAuth2Session
from django.utils import timezone
from datetime import timedelta
from PIL import Image
import tempfile
import boto3
import hashlib
from botocore.client import Config
import boto3
import pathlib
import imghdr
import re
import requests
import archieml

from search.indexes import PackageIndex

S3_BUCKET = settings.S3_ASSETS_UPLOAD_BUCKET
s3 = boto3.client('s3', 'us-west-2', config=Config(s3={'addressing_style': 'path'}))
PREFIX = "https://www.googleapis.com/drive"
IMAGE_REGEX = re.compile(r"!\[[^\]]+\]\(([^)]+)\)")

class PackageSet(models.Model):
    slug = models.SlugField(max_length=32, primary_key=True)
    drive_folder_id = models.CharField(max_length=512, blank=True)
    drive_folder_url = models.URLField()

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
    last_fetched_date = models.DateField(null=True, blank=True)
    package_set = models.ForeignKey(PackageSet, on_delete=models.PROTECT)
    
    # Versioning
    latest_version = models.ForeignKey('PackageVersion', related_name='versions', on_delete=models.CASCADE, null=True)


    # For versioning feature, accepts string arguments name(of creater) and change_summary
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
        
        # Versioning
        # self.create_version()

        return res.ok

    # TODO - put this in a workqueue
    def fetch_from_gdrive(self, user):
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
        except Exception as e:
            raise e
        finally:
            self.processing = False
            self.save()

        return self

# Snapshot of a Package instance at a particular time
class PackageVersion(models.Model):
    package = models.ForeignKey(Package, on_delete=models.PROTECT, null=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    version_description = models.TextField(blank=True)
    article_data = models.TextField(blank=True)
    data = JSONField(blank=True, default=dict, null=True)
    

def rewrite_image_url(package):
    def replace_url(fn):
        #print(fn.group(1).replace)
        if fn.group(1) in package.images["s3"]:
            return fn.group().replace(fn.group(1), package.images["s3"][fn.group(1)]["url"])
        else:
            return fn.group()
    text = IMAGE_REGEX.sub(replace_url,package.cached_article_preview)
    return text

def transfer_to_s3(session, package):
    if package.images.get("s3") is None:
        package.images["s3"] = {}

    for idx, image in enumerate(package.images["gdrive"]):
        req = get_file(session, image["id"], download=True)
        max_size = (1024, 1024)

        with tempfile.SpooledTemporaryFile(mode="w+b") as tf:
            print(image["title"] + " | Processing image %d ..." % idx)
            req.raw.decode_content = True
            header = req.raw.read(100)
            ext = imghdr.what(None, h=header)
            print(image["title"] + " | Found: {0}".format(ext))
            if ext == None:
                print("No image file found ... Continuing")
                continue

            tf.write(header + req.raw.read())
            im = Image.open(tf)
            image_hash = hashlib.md5(im.tobytes()).hexdigest()
            if image["title"] in package.images["s3"]:
                print("Old Hash found: " + package.images["s3"][image["title"]].get("hash"))
                print("Current Hash: " + image_hash)
                if package.images["s3"][image["title"]].get("hash") == image_hash:
                    print(image["title"] + " in package " + package.slug + " has not been edited. Ignoring.")
                    continue

            with tempfile.SpooledTemporaryFile(mode="w+b") as wtf:
                im.thumbnail(max_size, Image.ANTIALIAS)
                im.save(wtf, format=im.format, optimize=True, quality=85)
                original_fn = pathlib.Path(image["title"])
                fn = "images/{0}/{1}-{2}{3}".format(package.slug, original_fn.stem, image_hash, original_fn.suffix)
                wtf.seek(0)
                response = s3.put_object(
                    Bucket=S3_BUCKET,
                    Key=fn,
                    Body=wtf,
                    ACL='public-read'
                )

                package.images["s3"][image["title"]] = {
                    "url": "https://assets.dailybruin.com/{0}".format(fn), # TODO: replace with something configurable
                    "key": fn,
                    "hash": image_hash,
                    "s3_fields": response
                }
    return package


def add_to_repo_folder(session, package):
    payload = {
        "id": settings.REPOSITORY_FOLDER_ID
    }
    res = session.post(PREFIX + "/v2/files/" + package.drive_folder_id + "/parents", json=payload)
    return res.json()

def get_file(session, file_id, download=False):
    res = session.get(PREFIX + "/v2/files/" + file_id + ("?alt=media" if download else ""), stream=download)
    res.raise_for_status()
    if download:
        # Returns the requests object
        return res
    else:
        return res.json()

def list_folder(session, package):
    text = "### No article document was found in this package!\n"
    images = []

    payload = {
        "q": "'%s' in parents" % package.drive_folder_id,
        "maxResults": 1000
    }
    # we assume there's always less than 100 files in a package. change this if assumption untrue

    def img_check(item: dict):
        valid_extensions = [".jpeg", ".png", ".jpg", ".gif", ".webp"]
        for ext in valid_extensions:
            if ext in item["title"].lower():
                return True
        return False

    res = session.get(PREFIX + "/v2/files", params=payload)
    items = res.json()['items']
    article = list(filter(lambda f: "article" in f['title'], items))
    data_files = list(filter(lambda f: ".aml" in f['title'], items))
    images = list(filter(img_check, items))
    folders = list(filter(lambda f: f["mimeType"] == "application/vnd.google-apps.folder", items))
    #print("RES:")
    #print(article)
    #print(images)

    aml_data = {}

    # adds title of article as key, and parsed data as value. Saves info to aml_data

    for aml in data_files:
        if aml['mimeType'] != "application/vnd.google-apps.document":
            req = get_file(session, aml['id'], download=True)
            text = req.content.decode('utf-8')
        else:
            data = session.get(PREFIX + "/v2/files/" + aml['id'] + "/export", params={"mimeType": "text/plain"})
            text = data.content.decode('utf-8')
        #print("IN ARCHIEML ")
        aml_data[aml['title']] = archieml.loads(text)

    # only taking the first one - assuming there's only one article file
    if len(article) >= 1:
        if article[0]['mimeType'] != "application/vnd.google-apps.document":
            req = get_file(session, article[0]['id'], download=True)
            text = req.content.decode('utf-8')
        else:
            data = session.get(PREFIX + "/v2/files/" + article[0]['id'] + "/export", params={"mimeType": "text/plain"})
            text = data.content.decode('utf-8')
        # fix indentation for yaml
        text = text.replace("\t", "  ")
    # this will take REALLY long.

    # return everything
    return text, images, folders, aml_data

def create_package(session, package, existing=False):
    payload = {
        'parents': [{'id': settings.REPOSITORY_FOLDER_ID}],
        'title': package.slug,
        'description': package.description,
        'mimeType': "application/vnd.google-apps.folder"
    }

    res = session.post(PREFIX + "/v2/files", json=payload)
    folder_resource = res.json()

    file_payload = {
        'parents': [{'id': folder_resource['id']}],
        'title': "article.md",
        'description': "Article data",
        'mimeType': "application/vnd.google-apps.document"
    }
    session.post(PREFIX + "/v2/files", json=file_payload)

    return (folder_resource['alternateLink'], folder_resource['id'])


# https://github.com/pennersr/django-allauth/issues/420
def get_oauth2_session(user) -> OAuth2Session:
    """ Create OAuth2 session which autoupdates the access token if it has expired """

    refresh_token_url = "https://accounts.google.com/o/oauth2/token"

    social_token = SocialToken.objects.get(account__user=user, account__provider='google')

    def token_updater(token):
        social_token.token = token['access_token']
        social_token.token_secret = token['refresh_token']
        social_token.expires_at = timezone.now() + timedelta(seconds=int(token['expires_in']))
        social_token.save()

    client_id = social_token.app.client_id
    client_secret = social_token.app.secret

    extra = {
        'client_id': client_id,
        'client_secret': client_secret
    }

    expires_in = (social_token.expires_at - timezone.now()).total_seconds()
    token = {
        'access_token': social_token.token,
        'refresh_token': social_token.token_secret,
        'token_type': 'Bearer',
        'expires_in': expires_in  # Important otherwise the token update doesn't get triggered.
    }

    return OAuth2Session(client_id, token=token, auto_refresh_kwargs=extra,
                         auto_refresh_url=refresh_token_url, token_updater=token_updater)
