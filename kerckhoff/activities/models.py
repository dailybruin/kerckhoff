from enum import Enum

from django.contrib.postgres.fields import JSONField, ArrayField
from django.dispatch import receiver
from packages.models import PackageVersion

from .signals import package_updated, package_created

class ActivityType(Enum):
    PACKAGE_UPDATED: 'package_updated'
    PACKAGE_CREATED: 'package_created'

# Notes
    # **kwargs allows you to handle named arguments that you have not defined
    # in advance

    # the create method "creates" and "saves" the object in a single step

    # enum AcitivityType class created for cleaner code

class Activities(models.Model):
    # a dict that logs user actions
    user = models.ForeignKey(User)
    action = JSONField(blank=True, default=dict, null=True)

    # post_save is a signal that triggers this func log
    @receiver(post_save, sender=PackageVersion)
    def log(sender, instance: PackageVersion, created, **kwargs):
        if created:
            Activities.objects.create(user=instance.creator, action={
                "event_type": ActivityType.PACKAGE_CREATED,
                "data": {
                    "package_id": instance.package,
                    "commit_message": instance.version_description
                }
            })
        else:
            Activities.objects.create(user=instance.creator, action={
                "event_type": ActivityType.PACKAGE_UPDATED,
                "data": {
                    "package_id": instance.package,
                    "commit_message": instance.version_description
                }
            })