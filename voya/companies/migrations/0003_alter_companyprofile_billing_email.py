# Generated by Django 5.1.2 on 2024-11-06 10:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0002_alter_companyprofile_logo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='companyprofile',
            name='billing_email',
            field=models.EmailField(max_length=254, unique=True),
        ),
    ]
