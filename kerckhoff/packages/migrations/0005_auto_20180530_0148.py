# Generated by Django 2.0.5 on 2018-05-30 01:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('packages', '0004_auto_20180519_2151'),
    ]

    operations = [
        migrations.AlterField(
            model_name='package',
            name='last_fetched_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
