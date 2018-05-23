# Generated by Django 2.0.5 on 2018-05-19 21:51

from django.conf import settings
import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('packages', '0003_package_data'),
    ]

    operations = [
        migrations.CreateModel(
            name='PackageVersion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('version_description', models.TextField(blank=True)),
                ('article_data', models.TextField(blank=True)),
                ('data', django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=dict, null=True)),
                ('creator', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('package', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='packages.Package')),
            ],
        ),
        migrations.AddField(
            model_name='package',
            name='latest_version',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='versions', to='packages.PackageVersion'),
        ),
    ]