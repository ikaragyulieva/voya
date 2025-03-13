# Generated by Django 5.1.2 on 2025-03-10 12:46

import django.db.models.deletion
import django_countries.fields
import multiselectfield.db.fields
import simple_history.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0007_alter_companyprofile_commercial_name_and_more'),
        ('requests', '0022_alter_triprequests_city_destinations'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='HistoricalTripRequests',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('created_at', models.DateTimeField(blank=True, editable=False)),
                ('updated_at', models.DateTimeField(blank=True, editable=False)),
                ('country_origin', django_countries.fields.CountryField(max_length=2)),
                ('nationality', django_countries.fields.CountryField(max_length=2)),
                ('country_destinations', multiselectfield.db.fields.MultiSelectField(choices=[('', 'Select country'), ('AL', 'Albania'), ('AD', 'Andorra'), ('AM', 'Armenia'), ('AT', 'Austria'), ('AZ', 'Azerbaijan'), ('BY', 'Belarus'), ('BE', 'Belgium'), ('BA', 'Bosnia and Herzegovina'), ('BG', 'Bulgaria'), ('HR', 'Croatia'), ('CY', 'Cyprus'), ('CZ', 'Czech Republic'), ('DK', 'Denmark'), ('EE', 'Estonia'), ('FI', 'Finland'), ('FR', 'France'), ('GE', 'Georgia'), ('DE', 'Germany'), ('GR', 'Greece'), ('HU', 'Hungary'), ('IS', 'Iceland'), ('IE', 'Ireland'), ('IT', 'Italy'), ('XK', 'Kosovo'), ('LV', 'Latvia'), ('LI', 'Liechtenstein'), ('LT', 'Lithuania'), ('LU', 'Luxembourg'), ('MT', 'Malta'), ('MD', 'Moldova'), ('MC', 'Monaco'), ('ME', 'Montenegro'), ('NL', 'Netherlands'), ('MK', 'North Macedonia'), ('NO', 'Norway'), ('PL', 'Poland'), ('PT', 'Portugal'), ('RO', 'Romania'), ('SM', 'San Marino'), ('Scotland', 'Scotland'), ('RS', 'Serbia'), ('SK', 'Slovakia'), ('SI', 'Slovenia'), ('ES', 'Spain'), ('SE', 'Sweden'), ('CH', 'Switzerland'), ('TR', 'Turkey'), ('UA', 'Ukraine'), ('GB', 'United Kingdom'), ('VA', 'Vatican City'), ('DZ', 'Algeria'), ('EG', 'Egypt'), ('IL', 'Israel'), ('LB', 'Lebanon'), ('LY', 'Libya'), ('MA', 'Morocco'), ('PS', 'Palestine'), ('SY', 'Syria'), ('TN', 'Tunisia')], help_text='Choose the countries you would like to visit', max_length=100)),
                ('city_destinations', multiselectfield.db.fields.MultiSelectField(choices=[('', 'Select a city'), ('Generic', 'Generic city'), ('-', '-'), ('Amsterdam', 'Amsterdam'), ('Athens', 'Athens'), ('Ávila', 'Ávila'), ('Barcelona', 'Barcelona'), ('Belgrade', 'Belgrade'), ('Berlin', 'Berlin'), ('Bologna', 'Bologna'), ('Bordeaux', 'Bordeaux'), ('Bourges', 'Bourges'), ('Bruges', 'Bruges'), ('Brussels', 'Brussels'), ('Budapest', 'Budapest'), ('Cappadocia', 'Cappadocia'), ('Capri', 'Capri'), ('Chamonix', 'Chamonix'), ('Cinque Terre', 'Cinque Terre'), ('Coira/Chur', 'Coira/Chur'), ('Colmar', 'Colmar'), ('Como', 'Como'), ('Copenhagen', 'Copenhagen'), ('Cracow', 'Cracow'), ('Dublin', 'Dublin'), ('Dubrovnik', 'Dubrovnik'), ('Edinburgh', 'Edinburgh'), ('Fátima', 'Fátima'), ('Florence', 'Florence'), ('Frankfurt', 'Frankfurt'), ('Garbagnate Milanese', 'Garbagnate Milanese'), ('Geneva', 'Geneva'), ('Ghent', 'Ghent'), ('Glasgow', 'Glasgow'), ('Gothenburg', 'Gothenburg'), ('Harrogate', 'Harrogate'), ('Helsinki', 'Helsinki'), ('Highlands', 'Highlands'), ('Hvar', 'Hvar'), ('Ibiza', 'Ibiza'), ('Istanbul', 'Istanbul'), ('Lisbon', 'Lisbon'), ('Lisieux', 'Lisieux'), ('Liverpool', 'Liverpool'), ('Loire', 'Loire'), ('London', 'London'), ('Lourdes', 'Lourdes'), ('Lucerne', 'Lucerne'), ('Lyon', 'Lyon'), ('Madrid', 'Madrid'), ('Milan', 'Milan'), ('Montecatini Terme', 'Montecatini Terme'), ('Montserrat', 'Montserrat'), ('Moscow', 'Moscow'), ('Munich', 'Munich'), ('Mykonos', 'Mykonos'), ('Naples', 'Naples'), ('Nuremberg', 'Nuremberg'), ('Nice', 'Nice'), ('Oporto', 'Oporto'), ('Oslo', 'Oslo'), ('Pamplona', 'Pamplona'), ('Paris', 'Paris'), ('Prague', 'Prague'), ('Pisa', 'Pisa'), ('Reykjavik', 'Reykjavik'), ('Rome', 'Rome'), ('Salzburg', 'Salzburg'), ('Santiago de Compostela', 'Santiago de Compostela'), ('Santorini', 'Santorini'), ('Seville', 'Seville'), ('Sofia', 'Sofia'), ('Split', 'Split'), ('Stockholm', 'Stockholm'), ('Varna', 'Varna'), ('Venice', 'Venice'), ('Vienna', 'Vienna'), ('Vinci', 'Vinci'), ('Warsaw', 'Warsaw'), ('Zagreb', 'Zagreb'), ('Zaragoza', 'Zaragoza'), ('Zurich', 'Zurich'), ('Reims', 'Reims'), ('Grenoble', 'Grenoble'), ('Jerez de la Frontera', 'Jerez de la Frontera'), ('Chefchaouen', 'Chefchaouen'), ('Fez', 'Fez'), ('Rabat', 'Rabat'), ('Tanger', 'Tanger'), ('Tarragona', 'Tarragona'), ('Dudley', 'Dudley'), ('Leicester', 'Leicester'), ('Generic city', 'Generic city')], max_length=775)),
                ('other_destinations', models.CharField(blank=True, max_length=255, null=True)),
                ('budget', models.PositiveIntegerField()),
                ('trip_duration', models.PositiveIntegerField(blank=True, null=True)),
                ('trip_start_date', models.DateField()),
                ('trip_end_date', models.DateField()),
                ('age_range', models.PositiveIntegerField()),
                ('min_participants', models.PositiveIntegerField()),
                ('max_participants', models.PositiveIntegerField()),
                ('currency', models.CharField(choices=[('', 'Select an option'), ('eur', 'EUR'), ('usd', 'USD'), ('mxn', 'MXN'), ('chf', 'CHF')], default='currency', max_length=20)),
                ('transportation_type', models.CharField(choices=[('', 'Select an option'), ('no transportation', "No transportation - I'll take care of it"), ('private bus', 'Private Bus'), ('public buses', 'Public Buses'), ('trains', 'Trains'), ('flights', 'Flights'), ('taxi', 'Taxi'), ('airport/station transfers', 'Airport/Station Transfers')], default='transport', max_length=100)),
                ('transportation_details', models.CharField(blank=True, max_length=255, null=True)),
                ('accommodations', models.CharField(choices=[('acc', 'Select accommodations type'), ('none', "None -  I'll take care of it"), ('2-3 star hotels', '2-3 Star Hotels'), ('4-5 star hotels', '4-5 Star Hotels'), ('hostels with private bathroom', 'Hostels with private bathroom'), ('apartment', 'Apartment'), ('camping', 'Camping')], default='acc', max_length=100)),
                ('accommodations_details', models.CharField(blank=True, max_length=255, null=True)),
                ('meals', models.CharField(blank=True, choices=[('meal', 'Select meals service'), ('no meals included', 'No meals included'), ('breakfast only (BB)', 'Breakfast Only (BB)'), ('breakfast & dinner (HB)', 'Breakfast & Dinner (HB)'), ('breakfast, lunch & dinner (FB)', 'Breakfast, Lunch & Dinner (FB)')], default='meal', max_length=50, null=True)),
                ('meals_details', models.CharField(blank=True, max_length=255, null=True)),
                ('staff', models.CharField(blank=True, choices=[('staff', 'Select staff service'), ('Tour leader during the entire trip', 'Tour leader during the entire trip'), ('Official tourist guides in each city', 'Official Tourist Guides')], default='staff', max_length=50, null=True)),
                ('kind_of_group', models.CharField(blank=True, choices=[('group', 'Select type of group'), ('cultural_sightseeing', 'Cultural Group - Sightseeing'), ('schools_youth', 'Schools, Students or Youth'), ('backpackers', 'Backpackers'), ('theme_parks', 'Theme Parks (Eurodisney, Pinocchio, Mirabilandia, Puerto Aventura, Harry Potter...)'), ('study_language', 'Study or Language Package'), ('festivals_events', 'Festivals or Events'), ('sport', 'Sport'), ('family', 'Family'), ('religious', 'Religious'), ('relax_health_spas', 'Relax, Health, and SPAs'), ('adventure_nature', 'Adventure, Nature, Eco-tourism'), ('foodies_gastro_wine', 'Foodies - Gastro Tours - Wine Tours'), ('shopping', 'Shopping Tours'), ('yoga_meditation', 'Yoga or Meditation'), ('theme_tour', 'Theme Tour (Urban Art, Architecture, Science, Cinema...)'), ('photo_tours', 'Photo Tours'), ('cruises', 'Cruises')], default='group', max_length=100, null=True)),
                ('type_of_trip', models.CharField(blank=True, max_length=255, null=True)),
                ('additional_observations', models.CharField(blank=True, max_length=255, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('slug', models.SlugField(blank=True, editable=False)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('created_by_company', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='companies.companyprofile')),
                ('created_by_user', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical trip requests',
                'verbose_name_plural': 'historical trip requestss',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
    ]
