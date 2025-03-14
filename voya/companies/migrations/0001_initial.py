# Generated by Django 5.1.2 on 2024-11-04 10:46

import django.core.validators
import django.db.models.deletion
import django_countries.fields
import phonenumber_field.modelfields
import voya.companies.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CompanyProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('commercial_name', models.CharField(blank=True, max_length=255, null=True, unique=True, validators=[django.core.validators.MinLengthValidator(2)])),
                ('legal_name', models.CharField(blank=True, max_length=255, null=True, unique=True, validators=[django.core.validators.MinLengthValidator(2)])),
                ('tax_id', models.CharField(blank=True, max_length=15, null=True, unique=True, validators=[django.core.validators.MinLengthValidator(5)])),
                ('billing_email', models.EmailField(max_length=254)),
                ('country', django_countries.fields.CountryField(max_length=2)),
                ('logo', models.ImageField(upload_to='company_logos', validators=[voya.companies.validators.FileSizeValidator(5)])),
                ('notes', models.TextField(blank=True, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('street_address', models.CharField(max_length=255)),
                ('city', models.CharField(max_length=100)),
                ('state', models.CharField(blank=True, max_length=100, null=True)),
                ('postal_code', models.CharField(max_length=20, validators=[django.core.validators.MinLengthValidator(4)])),
                ('country', django_countries.fields.CountryField(max_length=2)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='addresses', to='companies.companyprofile')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PhoneNumber',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('number', phonenumber_field.modelfields.PhoneNumberField(help_text='Enter phone number in international format. Example: +123456789', max_length=128, region=None)),
                ('label', models.CharField(blank=True, max_length=50, null=True)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='phone_numbers', to='companies.companyprofile')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
