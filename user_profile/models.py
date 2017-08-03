# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class UserProfile(models.Model):
    CONTRIBUTOR = 'CT'
    PROJ_MANAGER = 'PM'
    SENIOR_STAFF = 'ST'
    ASST_EDITOR = 'AE'
    EDITOR = 'ED'
    ROLE_CHOICES = ( 
        (CONTRIBUTOR, 'Contributor'),
        (PROJ_MANAGER, 'Project Manager'),
        (SENIOR_STAFF, 'Senior Staff'),
        (ASST_EDITOR, 'Assistant Editor'),
        (EDITOR, 'Editor')
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, 
                                      primary_key=True)
    first_name = models.CharField(max_length=100, blank=True, default="")
    last_name = models.CharField(max_length=100, blank=True, default="")
    profile_img = models.ImageField(upload_to='profile/imgs/', 
                                    null=True)
    description = models.CharField(max_length=500, blank=True, default="")
    linkedin_url = models.URLField(blank=True, unique=True, default="")
    github_url = models.URLField(blank=True, unique=True, default="")
    role = models.CharField(
        max_length=2,
        choices=ROLE_CHOICES,
        default=CONTRIBUTOR,
    )


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance, 
                                   first_name=instance.first_name,
                                   last_name=instance.last_name)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()