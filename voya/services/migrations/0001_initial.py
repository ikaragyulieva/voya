# Generated by Django 5.1.2 on 2024-11-18 17:50

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Currency',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('currency', models.CharField(choices=[('currency', 'Select currency'), ('eur', 'EUR'), ('usd', 'USD'), ('mxn', 'MXN'), ('chf', 'CHF')], max_length=10)),
                ('exchange_rate', models.DecimalField(decimal_places=3, max_digits=5)),
                ('is_active', models.BooleanField(default=True)),
                ('created_by_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='currency_created_by', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Hotels',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('country', models.CharField(choices=[('AL', 'Albania'), ('AD', 'Andorra'), ('AM', 'Armenia'), ('AT', 'Austria'), ('AZ', 'Azerbaijan'), ('BY', 'Belarus'), ('BE', 'Belgium'), ('BA', 'Bosnia and Herzegovina'), ('BG', 'Bulgaria'), ('HR', 'Croatia'), ('CY', 'Cyprus'), ('CZ', 'Czech Republic'), ('DK', 'Denmark'), ('EE', 'Estonia'), ('FI', 'Finland'), ('FR', 'France'), ('GE', 'Georgia'), ('DE', 'Germany'), ('GR', 'Greece'), ('HU', 'Hungary'), ('IS', 'Iceland'), ('IE', 'Ireland'), ('IT', 'Italy'), ('XK', 'Kosovo'), ('LV', 'Latvia'), ('LI', 'Liechtenstein'), ('LT', 'Lithuania'), ('LU', 'Luxembourg'), ('MT', 'Malta'), ('MD', 'Moldova'), ('MC', 'Monaco'), ('ME', 'Montenegro'), ('NL', 'Netherlands'), ('MK', 'North Macedonia'), ('NO', 'Norway'), ('PL', 'Poland'), ('PT', 'Portugal'), ('RO', 'Romania'), ('SM', 'San Marino'), ('RS', 'Serbia'), ('SK', 'Slovakia'), ('SI', 'Slovenia'), ('ES', 'Spain'), ('SE', 'Sweden'), ('CH', 'Switzerland'), ('TR', 'Turkey'), ('UA', 'Ukraine'), ('GB', 'United Kingdom'), ('VA', 'Vatican City'), ('DZ', 'Algeria'), ('EG', 'Egypt'), ('IL', 'Israel'), ('LB', 'Lebanon'), ('LY', 'Libya'), ('MA', 'Morocco'), ('PS', 'Palestine'), ('SY', 'Syria'), ('TN', 'Tunisia')], max_length=100)),
                ('city', models.CharField(max_length=50)),
                ('capacity', models.IntegerField(default=1)),
                ('is_active', models.BooleanField(default=True)),
                ('category', models.CharField(choices=[('acc', 'Select accommodations type'), ('none', "None -  I'll take care of it"), ('2-3 star hotels', '2-3 Star Hotels'), ('4-5 star hotels', '4-5 Star Hotels'), ('hostels with private bathroom', 'Hostels with private bathroom'), ('apartment', 'Apartment'), ('camping', 'Camping')], max_length=30)),
                ('name', models.CharField(max_length=100)),
                ('high_season_price', models.DecimalField(decimal_places=2, max_digits=5)),
                ('low_season_price', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('created_by_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_created_by', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='LocalGuides',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('country', models.CharField(choices=[('AL', 'Albania'), ('AD', 'Andorra'), ('AM', 'Armenia'), ('AT', 'Austria'), ('AZ', 'Azerbaijan'), ('BY', 'Belarus'), ('BE', 'Belgium'), ('BA', 'Bosnia and Herzegovina'), ('BG', 'Bulgaria'), ('HR', 'Croatia'), ('CY', 'Cyprus'), ('CZ', 'Czech Republic'), ('DK', 'Denmark'), ('EE', 'Estonia'), ('FI', 'Finland'), ('FR', 'France'), ('GE', 'Georgia'), ('DE', 'Germany'), ('GR', 'Greece'), ('HU', 'Hungary'), ('IS', 'Iceland'), ('IE', 'Ireland'), ('IT', 'Italy'), ('XK', 'Kosovo'), ('LV', 'Latvia'), ('LI', 'Liechtenstein'), ('LT', 'Lithuania'), ('LU', 'Luxembourg'), ('MT', 'Malta'), ('MD', 'Moldova'), ('MC', 'Monaco'), ('ME', 'Montenegro'), ('NL', 'Netherlands'), ('MK', 'North Macedonia'), ('NO', 'Norway'), ('PL', 'Poland'), ('PT', 'Portugal'), ('RO', 'Romania'), ('SM', 'San Marino'), ('RS', 'Serbia'), ('SK', 'Slovakia'), ('SI', 'Slovenia'), ('ES', 'Spain'), ('SE', 'Sweden'), ('CH', 'Switzerland'), ('TR', 'Turkey'), ('UA', 'Ukraine'), ('GB', 'United Kingdom'), ('VA', 'Vatican City'), ('DZ', 'Algeria'), ('EG', 'Egypt'), ('IL', 'Israel'), ('LB', 'Lebanon'), ('LY', 'Libya'), ('MA', 'Morocco'), ('PS', 'Palestine'), ('SY', 'Syria'), ('TN', 'Tunisia')], max_length=100)),
                ('city', models.CharField(max_length=50)),
                ('capacity', models.IntegerField(default=1)),
                ('is_active', models.BooleanField(default=True)),
                ('guide_name', models.CharField(max_length=80)),
                ('price', models.DecimalField(decimal_places=2, max_digits=5)),
                ('price_includes', models.CharField(max_length=200)),
                ('tour_duration', models.CharField(blank=True, max_length=30, null=True)),
                ('created_by_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_created_by', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PrivateTransport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('country', models.CharField(choices=[('AL', 'Albania'), ('AD', 'Andorra'), ('AM', 'Armenia'), ('AT', 'Austria'), ('AZ', 'Azerbaijan'), ('BY', 'Belarus'), ('BE', 'Belgium'), ('BA', 'Bosnia and Herzegovina'), ('BG', 'Bulgaria'), ('HR', 'Croatia'), ('CY', 'Cyprus'), ('CZ', 'Czech Republic'), ('DK', 'Denmark'), ('EE', 'Estonia'), ('FI', 'Finland'), ('FR', 'France'), ('GE', 'Georgia'), ('DE', 'Germany'), ('GR', 'Greece'), ('HU', 'Hungary'), ('IS', 'Iceland'), ('IE', 'Ireland'), ('IT', 'Italy'), ('XK', 'Kosovo'), ('LV', 'Latvia'), ('LI', 'Liechtenstein'), ('LT', 'Lithuania'), ('LU', 'Luxembourg'), ('MT', 'Malta'), ('MD', 'Moldova'), ('MC', 'Monaco'), ('ME', 'Montenegro'), ('NL', 'Netherlands'), ('MK', 'North Macedonia'), ('NO', 'Norway'), ('PL', 'Poland'), ('PT', 'Portugal'), ('RO', 'Romania'), ('SM', 'San Marino'), ('RS', 'Serbia'), ('SK', 'Slovakia'), ('SI', 'Slovenia'), ('ES', 'Spain'), ('SE', 'Sweden'), ('CH', 'Switzerland'), ('TR', 'Turkey'), ('UA', 'Ukraine'), ('GB', 'United Kingdom'), ('VA', 'Vatican City'), ('DZ', 'Algeria'), ('EG', 'Egypt'), ('IL', 'Israel'), ('LB', 'Lebanon'), ('LY', 'Libya'), ('MA', 'Morocco'), ('PS', 'Palestine'), ('SY', 'Syria'), ('TN', 'Tunisia')], max_length=100)),
                ('city', models.CharField(max_length=50)),
                ('capacity', models.IntegerField(default=1)),
                ('is_active', models.BooleanField(default=True)),
                ('type', models.CharField(choices=[('transport', 'Select transportation type'), ('no transportation', "No transportation - I'll take care of it"), ('private bus', 'Private Bus'), ('public buses', 'Public Buses'), ('trains', 'Trains'), ('flights', 'Flights'), ('taxi', 'Taxi'), ('airport/station transfers', 'Airport/Station Transfers')], max_length=30)),
                ('price', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('created_by_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_created_by', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PublicTransport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('country', models.CharField(choices=[('AL', 'Albania'), ('AD', 'Andorra'), ('AM', 'Armenia'), ('AT', 'Austria'), ('AZ', 'Azerbaijan'), ('BY', 'Belarus'), ('BE', 'Belgium'), ('BA', 'Bosnia and Herzegovina'), ('BG', 'Bulgaria'), ('HR', 'Croatia'), ('CY', 'Cyprus'), ('CZ', 'Czech Republic'), ('DK', 'Denmark'), ('EE', 'Estonia'), ('FI', 'Finland'), ('FR', 'France'), ('GE', 'Georgia'), ('DE', 'Germany'), ('GR', 'Greece'), ('HU', 'Hungary'), ('IS', 'Iceland'), ('IE', 'Ireland'), ('IT', 'Italy'), ('XK', 'Kosovo'), ('LV', 'Latvia'), ('LI', 'Liechtenstein'), ('LT', 'Lithuania'), ('LU', 'Luxembourg'), ('MT', 'Malta'), ('MD', 'Moldova'), ('MC', 'Monaco'), ('ME', 'Montenegro'), ('NL', 'Netherlands'), ('MK', 'North Macedonia'), ('NO', 'Norway'), ('PL', 'Poland'), ('PT', 'Portugal'), ('RO', 'Romania'), ('SM', 'San Marino'), ('RS', 'Serbia'), ('SK', 'Slovakia'), ('SI', 'Slovenia'), ('ES', 'Spain'), ('SE', 'Sweden'), ('CH', 'Switzerland'), ('TR', 'Turkey'), ('UA', 'Ukraine'), ('GB', 'United Kingdom'), ('VA', 'Vatican City'), ('DZ', 'Algeria'), ('EG', 'Egypt'), ('IL', 'Israel'), ('LB', 'Lebanon'), ('LY', 'Libya'), ('MA', 'Morocco'), ('PS', 'Palestine'), ('SY', 'Syria'), ('TN', 'Tunisia')], max_length=100)),
                ('city', models.CharField(max_length=50)),
                ('capacity', models.IntegerField(default=1)),
                ('is_active', models.BooleanField(default=True)),
                ('type', models.CharField(choices=[('transport', 'Select transportation type'), ('no transportation', "No transportation - I'll take care of it"), ('private bus', 'Private Bus'), ('public buses', 'Public Buses'), ('trains', 'Trains'), ('flights', 'Flights'), ('taxi', 'Taxi'), ('airport/station transfers', 'Airport/Station Transfers')], max_length=30)),
                ('price', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('created_by_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_created_by', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Tickets',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('country', models.CharField(choices=[('AL', 'Albania'), ('AD', 'Andorra'), ('AM', 'Armenia'), ('AT', 'Austria'), ('AZ', 'Azerbaijan'), ('BY', 'Belarus'), ('BE', 'Belgium'), ('BA', 'Bosnia and Herzegovina'), ('BG', 'Bulgaria'), ('HR', 'Croatia'), ('CY', 'Cyprus'), ('CZ', 'Czech Republic'), ('DK', 'Denmark'), ('EE', 'Estonia'), ('FI', 'Finland'), ('FR', 'France'), ('GE', 'Georgia'), ('DE', 'Germany'), ('GR', 'Greece'), ('HU', 'Hungary'), ('IS', 'Iceland'), ('IE', 'Ireland'), ('IT', 'Italy'), ('XK', 'Kosovo'), ('LV', 'Latvia'), ('LI', 'Liechtenstein'), ('LT', 'Lithuania'), ('LU', 'Luxembourg'), ('MT', 'Malta'), ('MD', 'Moldova'), ('MC', 'Monaco'), ('ME', 'Montenegro'), ('NL', 'Netherlands'), ('MK', 'North Macedonia'), ('NO', 'Norway'), ('PL', 'Poland'), ('PT', 'Portugal'), ('RO', 'Romania'), ('SM', 'San Marino'), ('RS', 'Serbia'), ('SK', 'Slovakia'), ('SI', 'Slovenia'), ('ES', 'Spain'), ('SE', 'Sweden'), ('CH', 'Switzerland'), ('TR', 'Turkey'), ('UA', 'Ukraine'), ('GB', 'United Kingdom'), ('VA', 'Vatican City'), ('DZ', 'Algeria'), ('EG', 'Egypt'), ('IL', 'Israel'), ('LB', 'Lebanon'), ('LY', 'Libya'), ('MA', 'Morocco'), ('PS', 'Palestine'), ('SY', 'Syria'), ('TN', 'Tunisia')], max_length=100)),
                ('city', models.CharField(max_length=50)),
                ('capacity', models.IntegerField(default=1)),
                ('is_active', models.BooleanField(default=True)),
                ('name', models.CharField(max_length=50)),
                ('price_per_person', models.DecimalField(decimal_places=2, max_digits=5)),
                ('description', models.TextField(blank=True, null=True)),
                ('created_by_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_created_by', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Transfers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('country', models.CharField(choices=[('AL', 'Albania'), ('AD', 'Andorra'), ('AM', 'Armenia'), ('AT', 'Austria'), ('AZ', 'Azerbaijan'), ('BY', 'Belarus'), ('BE', 'Belgium'), ('BA', 'Bosnia and Herzegovina'), ('BG', 'Bulgaria'), ('HR', 'Croatia'), ('CY', 'Cyprus'), ('CZ', 'Czech Republic'), ('DK', 'Denmark'), ('EE', 'Estonia'), ('FI', 'Finland'), ('FR', 'France'), ('GE', 'Georgia'), ('DE', 'Germany'), ('GR', 'Greece'), ('HU', 'Hungary'), ('IS', 'Iceland'), ('IE', 'Ireland'), ('IT', 'Italy'), ('XK', 'Kosovo'), ('LV', 'Latvia'), ('LI', 'Liechtenstein'), ('LT', 'Lithuania'), ('LU', 'Luxembourg'), ('MT', 'Malta'), ('MD', 'Moldova'), ('MC', 'Monaco'), ('ME', 'Montenegro'), ('NL', 'Netherlands'), ('MK', 'North Macedonia'), ('NO', 'Norway'), ('PL', 'Poland'), ('PT', 'Portugal'), ('RO', 'Romania'), ('SM', 'San Marino'), ('RS', 'Serbia'), ('SK', 'Slovakia'), ('SI', 'Slovenia'), ('ES', 'Spain'), ('SE', 'Sweden'), ('CH', 'Switzerland'), ('TR', 'Turkey'), ('UA', 'Ukraine'), ('GB', 'United Kingdom'), ('VA', 'Vatican City'), ('DZ', 'Algeria'), ('EG', 'Egypt'), ('IL', 'Israel'), ('LB', 'Lebanon'), ('LY', 'Libya'), ('MA', 'Morocco'), ('PS', 'Palestine'), ('SY', 'Syria'), ('TN', 'Tunisia')], max_length=100)),
                ('city', models.CharField(max_length=50)),
                ('capacity', models.IntegerField(default=1)),
                ('is_active', models.BooleanField(default=True)),
                ('car_price_city', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('car_price_airport', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('bus_price_city', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('bus_price_airport', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('created_by_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_created_by', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
