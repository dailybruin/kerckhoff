from rest_framework import serializers, viewsets

from .models import PackageSet


class PackageSetSerializer(serializers.ModelSerializer):
    class Meta:
        model = PackageSet
        fields = ("slug", "drive_folder_id", "drive_folder_url", "default_content_type")
