from rest_framework import serializers
from .models import UserProfile


class UserProfileSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = UserProfile
        fields = (
            "first_name",
            "email",
            "profile_picture_path",
            "bio",
            "github_link",
            "linkedin_link",
        )
