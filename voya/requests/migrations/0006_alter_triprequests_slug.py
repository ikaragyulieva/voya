# Generated by Django 5.1.2 on 2024-11-11 20:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('requests', '0005_alter_triprequests_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='triprequests',
            name='slug',
            field=models.SlugField(blank=True, default=0.00045267489711934157, editable=False, unique=True),
            preserve_default=False,
        ),
    ]
