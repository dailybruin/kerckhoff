from django.db import models
from django.contrib.postgres.fields import JSONField, ArrayField
from allauth.socialaccount.models import SocialToken
from requests_oauthlib import OAuth2Session
from django.utils import timezone
from datetime import timedelta
from django.conf import settings

PREFIX = "https://www.googleapis.com/drive"

class Package(models.Model):
    slug = models.CharField(max_length=64, primary_key=True)
    description = models.TextField()
    drive_folder_id = models.CharField(max_length=512)
    drive_folder_url = models.URLField()
    images = ArrayField(JSONField(), default=list, blank=True)
    processing = models.BooleanField(default=False)
    cached_article_preview = models.TextField()
    publish_date = models.DateField()
    last_fetched_date = models.DateField(null=True, blank=True)

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
            self.drive_folder_id = self.drive_folder_url.rsplit('/', 1)[-1]
        self.cached_article_preview = ""
        self.images = []
        self.save()
        return self

    # TODO - put this in a workqueue
    def fetch_from_gdrive(self, user):
        google = get_oauth2_session(user)
        text, images = list_folder(google, self)
        self.cached_article_preview = text[3:]
        self.images = images
        self.save()
        return self

def img_check(filename):
    valid_extensions = [".jpeg", ".png", ".jpg", ".gif", ".webp"]
    for ext in valid_extensions:
        if ext in filename:
            return True
    return False

def list_folder(session, package):
    
    text = """### No article document was found in this package!\n""",
    images = []
    
    payload = {
        "q": "'%s' in parents" % package.drive_folder_id
    }
    # we assume there's always less than 100 files in a package. change this if assumption untrue
    res = session.get(PREFIX + "/v2/files", params=payload)
    print("RES:")
    items = res.json()['items']
    article = list(filter(lambda f: "article" in f['title'], items))
    images = list(filter(img_check, items))

    print(article)
    print(images)

    # only taking the first one - assuming there's only one article file
    if len(article) >= 1:
        data = session.get(PREFIX + "/v2/files/" + article[0]['id'] + "/export", params={"mimeType": "text/plain"})
        text = data.text

    return text, images

def create_package(session, package):
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
