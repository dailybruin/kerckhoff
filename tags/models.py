from django.db import models

# Create your models here.
class Tags(models.Model):
    value = models.CharField(max_length=64)

    def __str__(self):
        return self.value
        