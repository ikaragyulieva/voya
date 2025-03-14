# Generated by Django 5.1.2 on 2024-11-19 11:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='currency',
            old_name='currency',
            new_name='currency_from',
        ),
        migrations.RenameField(
            model_name='tickets',
            old_name='price_per_person',
            new_name='price',
        ),
        migrations.AddField(
            model_name='currency',
            name='currency_to',
            field=models.CharField(choices=[('currency', 'Select currency'), ('eur', 'EUR'), ('usd', 'USD'), ('mxn', 'MXN'), ('chf', 'CHF')], default='eur', max_length=10),
        ),
    ]
