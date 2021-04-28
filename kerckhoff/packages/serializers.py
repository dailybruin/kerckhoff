from rest_framework import serializers, viewsets

from .models import PackageSet, Package, PackageVersion


class PackageSetSerializer(serializers.ModelSerializer):
    class Meta:
        model = PackageSet
        fields = ("slug", "drive_folder_id", "drive_folder_url", "default_content_type")

class PackageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Package
        fields = "__all__"

class PackageVersionSerializer(serializers.ModelSerializer):
    package_slug = serializers.ReadOnlyField(source='package.slug')

    class Meta:
        model = PackageVersion
        fields = "__all__"