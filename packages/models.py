from django.db import models
from django.contrib.postgres.fields import JSONField, ArrayField
from allauth.socialaccount.models import SocialToken
from requests_oauthlib import OAuth2Session
from django.utils import timezone
from datetime import timedelta
from django.conf import settings
from django.core.exceptions import ValidationError
from PIL import Image
import tempfile
import boto3
import hashlib
from botocore.client import Config
import boto3
import pathlib
import imghdr
import CloudFlare
import re

S3_BUCKET = settings.S3_ASSETS_UPLOAD_BUCKET
s3 = boto3.client('s3', 'us-west-2', config=Config(s3={'addressing_style': 'path'}))
PREFIX = "https://www.googleapis.com/drive"
cf = CloudFlare.CloudFlare()
IMAGE_REGEX = re.compile(r"!\[[^\]]+\]\(([^)]+)\)")

#class PackageSet(models.Model):
#    slug = models.SlugField(max_length=32, primary_key=True)
#    drive_folder_url = models.URLField()
#    drive_folder_id = models.CharField(max_length=512)
#    def setup_and_save(self, user):


class Package(models.Model):
    slug = models.CharField(max_length=64, primary_key=True)
    description = models.TextField()
    drive_folder_id = models.CharField(max_length=512)
    drive_folder_url = models.URLField()
    metadata = JSONField(blank=True, default=dict, null=True)
    images = JSONField(blank=True, default=dict, null=True)
    processing = models.BooleanField(default=False)
    cached_article_preview = models.TextField()
    publish_date = models.DateField()
    last_fetched_date = models.DateField(null=True, blank=True)
#    package_set = models.ForeignKey(PackageSet, on_delete=models.PROTECT)

    def as_dict(self):
        return {
            "slug": self.slug,
            "description": self.description,
            "gdrive_url": self.drive_folder_url,
            "images": self.images,
            "article": self.cached_article_preview,
            "publish_date": self.publish_date,
            "last_fetched_date": self.last_fetched_date
        }

    def setup_and_save(self, user):
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
        self.images = []
        self.save()
        return self

    # TODO - put this in a workqueue
    def fetch_from_gdrive(self, user):
        self.processing = True
        self.save()

        try:
            google = get_oauth2_session(user)
            text, images = list_folder(google, self)
            self.cached_article_preview = text[3:]
            if self.images is None:
                self.images = {}
            self.images["gdrive"] = images
            transfer_to_s3(google, self)
            self.last_fetched_date = timezone.now()
        except Exception as e:
            raise e
        finally:
            self.processing = False
            self.save()

        return self

#def rewrite_image_url(package):
#    IMAGE_REGEX.findall(package.cached_article_preview)


def img_check(item):
    valid_extensions = [".jpeg", ".png", ".jpg", ".gif", ".webp"]
    for ext in valid_extensions:
        if ext in item['title']:
            return True
    return False

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
    text = "...### No article document was found in this package!\n"
    images = []
    
    payload = {
        "q": "'%s' in parents" % package.drive_folder_id
    }
    # we assume there's always less than 100 files in a package. change this if assumption untrue
    res = session.get(PREFIX + "/v2/files", params=payload)
    items = res.json()['items']
    article = list(filter(lambda f: "article" in f['title'], items))
    images = list(filter(img_check, items))
    #print("RES:")
    #print(article)
    #print(images)

    # only taking the first one - assuming there's only one article file
    if len(article) >= 1:
        data = session.get(PREFIX + "/v2/files/" + article[0]['id'] + "/export", params={"mimeType": "text/plain"})
        text = data.text
    # this will take REALLY long.
    return text, images

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
def get_oauth2_session(user):
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
