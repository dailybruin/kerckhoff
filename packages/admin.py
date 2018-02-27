from django.contrib import admin

# Register your models here.

from .models import Package

admin.site.register(Package)
