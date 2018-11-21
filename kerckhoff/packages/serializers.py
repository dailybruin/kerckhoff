from rest_framework import serializers, viewsets

from .models import PackageSet, Package, PackageVersion


class PackageSetSerializer(serializers.ModelSerializer):
    class Meta:
        model = PackageSet
        fields = ("slug", "drive_folder_id", "drive_folder_url", "default_content_type")

class PackageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Package
        fields = ("slug", "description", "drive_folder_id", "drive_folder_url",
                    "metadata", "images", "data", "processing", "cached_article_preview",
                    "publish_date", "last_fetched_date", "package_set", "_content_type",
                    "created_at", "updated_at", "latest_version")

class PackageVersionSerializer(serializers.ModelSerializer):
    package_slug = serializers.ReadOnlyField(source='package.slug')

    class Meta:
        model = PackageVersion
        fields = ("__all__")