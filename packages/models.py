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
    images = ArrayField(JSONField(), default=list)
    processing = models.BooleanField(default=False)
    cached_article_preview = models.TextField()
    publish_date = models.DateField()
    last_fetched_date = models.DateField(null=True)

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
        self.cached_article_preview = ""
        self.images = []
        self.save()
        return self

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
