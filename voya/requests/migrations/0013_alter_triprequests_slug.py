# Generated by Django 5.1.2 on 2024-12-11 21:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('requests', '0012_alter_triprequests_city_destinations'),
    ]

    operations = [
        migrations.AlterField(
            model_name='triprequests',
            name='slug',
            field=models.SlugField(blank=True, editable=False),
        ),
    ]