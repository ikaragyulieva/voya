# Generated by Django 5.1.2 on 2025-02-27 14:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proposals', '0015_alter_proposalbudget_free_of_charge'),
    ]

    operations = [
        migrations.AlterField(
            model_name='proposalsectionitem',
            name='section_name',
            field=models.CharField(choices=[('Accommodations', 'Accommodations'), ('Public Transport', 'Public Transport'), ('Private Transport', 'Private Transport'), ('Transfers', 'Transfers'), ('Activity', 'Activity'), ('Local Guides', 'Local Guides'), ('Tour Leader', 'Tour Leader'), ('Other Services', 'Other Services')], max_length=50),
        ),
    ]
