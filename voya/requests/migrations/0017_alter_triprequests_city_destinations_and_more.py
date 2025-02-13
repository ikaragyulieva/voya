# Generated by Django 5.1.2 on 2025-02-13 12:11

import multiselectfield.db.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('requests', '0016_alter_triprequests_country_destinations'),
    ]

    operations = [
        migrations.AlterField(
            model_name='triprequests',
            name='city_destinations',
            field=multiselectfield.db.fields.MultiSelectField(choices=[('', 'Select a city'), ('Amsterdam', 'Amsterdam'), ('Athens', 'Athens'), ('Barcelona', 'Barcelona'), ('Belgrade', 'Belgrade'), ('Berlin', 'Berlin'), ('Bruges', 'Bruges'), ('Brussels', 'Brussels'), ('Budapest', 'Budapest'), ('Copenhagen', 'Copenhagen'), ('Dublin', 'Dublin'), ('Edinburgh', 'Edinburgh'), ('Florence', 'Florence'), ('Geneva', 'Geneva'), ('Helsinki', 'Helsinki'), ('Istanbul', 'Istanbul'), ('Lisbon', 'Lisbon'), ('London', 'London'), ('Lucerne', 'Lucerne'), ('Madrid', 'Madrid'), ('Milan', 'Milan'), ('Moscow', 'Moscow'), ('Munich', 'Munich'), ('Naples', 'Naples'), ('Nice', 'Nice'), ('Oslo', 'Oslo'), ('Paris', 'Paris'), ('Prague', 'Prague'), ('Pisa', 'Pisa'), ('Reykjavik', 'Reykjavik'), ('Rome', 'Rome'), ('Salzburg', 'Salzburg'), ('Santorini', 'Santorini'), ('Seville', 'Seville'), ('Sofia', 'Sofia'), ('Split', 'Split'), ('Stockholm', 'Stockholm'), ('Varna', 'Varna'), ('Venice', 'Venice'), ('Vienna', 'Vienna'), ('Warsaw', 'Warsaw'), ('Zagreb', 'Zagreb'), ('Zurich', 'Zurich')], max_length=319),
        ),
        migrations.AlterField(
            model_name='triprequests',
            name='country_destinations',
            field=multiselectfield.db.fields.MultiSelectField(choices=[('', 'Select country'), ('AL', 'Albania'), ('AD', 'Andorra'), ('AM', 'Armenia'), ('AT', 'Austria'), ('AZ', 'Azerbaijan'), ('BY', 'Belarus'), ('BE', 'Belgium'), ('BA', 'Bosnia and Herzegovina'), ('BG', 'Bulgaria'), ('HR', 'Croatia'), ('CY', 'Cyprus'), ('CZ', 'Czech Republic'), ('DK', 'Denmark'), ('EE', 'Estonia'), ('FI', 'Finland'), ('FR', 'France'), ('GE', 'Georgia'), ('DE', 'Germany'), ('GR', 'Greece'), ('HU', 'Hungary'), ('IS', 'Iceland'), ('IE', 'Ireland'), ('IT', 'Italy'), ('XK', 'Kosovo'), ('LV', 'Latvia'), ('LI', 'Liechtenstein'), ('LT', 'Lithuania'), ('LU', 'Luxembourg'), ('MT', 'Malta'), ('MD', 'Moldova'), ('MC', 'Monaco'), ('ME', 'Montenegro'), ('NL', 'Netherlands'), ('MK', 'North Macedonia'), ('NO', 'Norway'), ('PL', 'Poland'), ('PT', 'Portugal'), ('RO', 'Romania'), ('SM', 'San Marino'), ('RS', 'Serbia'), ('SK', 'Slovakia'), ('SI', 'Slovenia'), ('ES', 'Spain'), ('SE', 'Sweden'), ('CH', 'Switzerland'), ('TR', 'Turkey'), ('UA', 'Ukraine'), ('GB', 'United Kingdom'), ('VA', 'Vatican City'), ('DZ', 'Algeria'), ('EG', 'Egypt'), ('IL', 'Israel'), ('LB', 'Lebanon'), ('LY', 'Libya'), ('MA', 'Morocco'), ('PS', 'Palestine'), ('SY', 'Syria'), ('TN', 'Tunisia')], help_text='Choose the countries you would like to visit', max_length=100),
        ),
        migrations.AlterField(
            model_name='triprequests',
            name='currency',
            field=models.CharField(choices=[('', 'Select an option'), ('eur', 'EUR'), ('usd', 'USD'), ('mxn', 'MXN'), ('chf', 'CHF')], default='currency', max_length=20),
        ),
        migrations.AlterField(
            model_name='triprequests',
            name='transportation_type',
            field=models.CharField(choices=[('', 'Select an option'), ('no transportation', "No transportation - I'll take care of it"), ('private bus', 'Private Bus'), ('public buses', 'Public Buses'), ('trains', 'Trains'), ('flights', 'Flights'), ('taxi', 'Taxi'), ('airport/station transfers', 'Airport/Station Transfers')], default='transport', max_length=100),
        ),
    ]
