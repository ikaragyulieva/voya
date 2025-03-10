# Generated by Django 5.1.2 on 2024-11-10 18:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0003_alter_companyprofile_billing_email'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='companyprofile',
            name='country',
        ),
        migrations.RemoveField(
            model_name='phonenumber',
            name='label',
        ),
        migrations.AddField(
            model_name='address',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='companyprofile',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='phonenumber',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
