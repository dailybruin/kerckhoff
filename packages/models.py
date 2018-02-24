from django.db import models
from django.contrib.postgres.fields import JSONField, ArrayField
from pydrive.drive import GoogleDrive
from pydrive.auth import GoogleAuth
from allauth.socialaccount.models import SocialToken

class Package(models.Model):
    slug = models.CharField(max_length=64, primary_key=True)
    description = models.TextField()
    drive_folder_id = models.CharField(max_length=512)
    drive_folder_url = models.URLField()
    images = ArrayField(JSONField(), default=list)
    cached_article_preview = models.TextField()
    publish_date = models.DateField()

    def setup_and_save(self, user):
        gauth = GoogleAuth()
        token = SocialToken.objects.get(account__user=user, account__provider='google')
        gauth.Auth(token)
        drive = GoogleDrive(gauth)
        file_list = drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
        for file1 in file_list:
            print('title: %s, id: %s' % (file1['title'], file1['id']))
