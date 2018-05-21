from django.contrib import admin

# Register your models here.

from .models import Package, PackageSet

def update(modeladmin, request, queryset):
    for pset in queryset:
        pset.populate(request.user)

update.short_description = "Updates Packages from Google Drive"

class PackageSetAdmin(admin.ModelAdmin):
    actions = [update,]

admin.site.register(Package)
admin.site.register(PackageSet, PackageSetAdmin)