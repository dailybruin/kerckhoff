from typing import List

from django.contrib import admin

from .models import Package, PackageSet

# Register your models here.


def update(modeladmin, request, queryset: List[PackageSet]):
    for pset in queryset:
        pset.populate(request.user, update_packages=True)


update.short_description = "Updates Packages from Google Drive"


class PackageSetAdmin(admin.ModelAdmin):
    actions = [update]


admin.site.register(Package)
admin.site.register(PackageSet, PackageSetAdmin)
