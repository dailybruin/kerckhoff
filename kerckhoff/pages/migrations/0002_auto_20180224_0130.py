# Generated by Django 2.0.2 on 2018-02-24 01:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='page',
            name='current_release',
        ),
        migrations.RemoveField(
            model_name='release',
            name='uploaded_files',
        ),
        migrations.AddField(
            model_name='release',
            name='hash_str',
            field=models.CharField(default='1a11', max_length=48),
            preserve_default=False,
        ),
    ]