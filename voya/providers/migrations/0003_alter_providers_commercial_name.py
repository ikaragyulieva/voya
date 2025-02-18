# Generated by Django 5.1.2 on 2025-02-18 21:37

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('providers', '0002_alter_providers_country_alter_providers_email_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='providers',
            name='commercial_name',
            field=models.CharField(default='test', max_length=100, validators=[django.core.validators.MinLengthValidator(2)]),
            preserve_default=False,
        ),
    ]
