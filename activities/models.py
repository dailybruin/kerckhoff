from django.db import models
from django.contrib.postgres.fields import JSONField, ArrayField
from django.dispatch import receiver

from .signals import package_updated

# Notes
    # **kwargs allows you to handle named arguments that you have not defined
    # in advance

class Activities(models.Model):
    # a dict that logs user actions
    action = JSONField(blank=True, default=dict, null=True)
    user = models.ForeignKey(User)

    # post_save is a signal that triggers this func log
    @receiver(post_save, sender=User)
    def log(sender, instance, created, **kwargs):
        if created:
            Activities.objects.create(user=instance,action={
                "event_type": "user_saved",
                "package_id": ,
            })

    @receiver(package_updated)
    def log_package_update
        Activities.objects.create()
