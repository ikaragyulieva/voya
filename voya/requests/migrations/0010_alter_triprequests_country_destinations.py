# Generated by Django 5.1.2 on 2024-11-14 13:09

import multiselectfield.db.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('requests', '0009_alter_triprequests_accommodations_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='triprequests',
            name='country_destinations',
            field=multiselectfield.db.fields.MultiSelectField(choices=[('AL', 'Albania'), ('AD', 'Andorra'), ('AM', 'Armenia'), ('AT', 'Austria'), ('AZ', 'Azerbaijan'), ('BY', 'Belarus'), ('BE', 'Belgium'), ('BA', 'Bosnia and Herzegovina'), ('BG', 'Bulgaria'), ('HR', 'Croatia'), ('CY', 'Cyprus'), ('CZ', 'Czech Republic'), ('DK', 'Denmark'), ('EE', 'Estonia'), ('FI', 'Finland'), ('FR', 'France'), ('GE', 'Georgia'), ('DE', 'Germany'), ('GR', 'Greece'), ('HU', 'Hungary'), ('IS', 'Iceland'), ('IE', 'Ireland'), ('IT', 'Italy'), ('XK', 'Kosovo'), ('LV', 'Latvia'), ('LI', 'Liechtenstein'), ('LT', 'Lithuania'), ('LU', 'Luxembourg'), ('MT', 'Malta'), ('MD', 'Moldova'), ('MC', 'Monaco'), ('ME', 'Montenegro'), ('NL', 'Netherlands'), ('MK', 'North Macedonia'), ('NO', 'Norway'), ('PL', 'Poland'), ('PT', 'Portugal'), ('RO', 'Romania'), ('SM', 'San Marino'), ('RS', 'Serbia'), ('SK', 'Slovakia'), ('SI', 'Slovenia'), ('ES', 'Spain'), ('SE', 'Sweden'), ('CH', 'Switzerland'), ('TR', 'Turkey'), ('UA', 'Ukraine'), ('GB', 'United Kingdom'), ('VA', 'Vatican City'), ('DZ', 'Algeria'), ('EG', 'Egypt'), ('IL', 'Israel'), ('LB', 'Lebanon'), ('LY', 'Libya'), ('MA', 'Morocco'), ('PS', 'Palestine'), ('SY', 'Syria'), ('TN', 'Tunisia')], help_text='Choose the countries you would like to visit', max_length=100),
        ),
    ]