# Generated by Django 5.1.2 on 2024-11-10 18:41

import phonenumber_field.modelfields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0003_remove_employeeprofile_label_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employeeprofile',
            name='phone_number',
            field=phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None),
        ),
    ]