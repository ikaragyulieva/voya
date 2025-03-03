# Generated by Django 5.1.2 on 2025-02-18 21:37

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0006_alter_companyprofile_logo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='companyprofile',
            name='commercial_name',
            field=models.CharField(default='test', max_length=255, unique=True, validators=[django.core.validators.MinLengthValidator(2)]),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='companyprofile',
            name='legal_name',
            field=models.CharField(default='test', max_length=255, unique=True, validators=[django.core.validators.MinLengthValidator(2)]),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='companyprofile',
            name='tax_id',
            field=models.CharField(default=1234, max_length=15, unique=True, validators=[django.core.validators.MinLengthValidator(5)]),
            preserve_default=False,
        ),
    ]
