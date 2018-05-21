from django.contrib import admin

# Register your models here.

from .models import Page
from .models import Series
from .models import Release

admin.site.register(Page)
admin.site.register(Series)
admin.site.register(Release)
