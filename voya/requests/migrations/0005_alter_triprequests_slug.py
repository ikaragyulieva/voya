# Generated by Django 5.1.2 on 2024-11-11 19:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('requests', '0004_triprequests_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='triprequests',
            name='slug',
            field=models.SlugField(blank=True, editable=False, null=True),
        ),
    ]
