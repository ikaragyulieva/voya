# Generated by Django 5.1.2 on 2025-03-05 13:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proposals', '0017_alter_proposalsectionitem_city'),
    ]

    operations = [
        migrations.AlterField(
            model_name='proposalsectionitem',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
    ]
