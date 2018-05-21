from django import forms
from django.forms import ModelForm

from .models import Package

class PackageForm(ModelForm):

    drive_folder_url = forms.URLField(required=False)

    class Meta:
        model = Package
        fields = ['slug', 'description', 'drive_folder_url', 'publish_date']

