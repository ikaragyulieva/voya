# Generated by Django 5.1.2 on 2024-11-13 16:00

import multiselectfield.db.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('requests', '0006_alter_triprequests_slug'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='triprequests',
            name='title',
        ),
        migrations.AlterField(
            model_name='triprequests',
            name='accommodations_details',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='triprequests',
            name='additional_observations',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='triprequests',
            name='city_destinations',
            field=multiselectfield.db.fields.MultiSelectField(choices=[('Amsterdam', 'Amsterdam'), ('Athens', 'Athens'), ('Barcelona', 'Barcelona'), ('Belgrade', 'Belgrade'), ('Berlin', 'Berlin'), ('Bruges', 'Bruges'), ('Brussels', 'Brussels'), ('Budapest', 'Budapest'), ('Copenhagen', 'Copenhagen'), ('Dublin', 'Dublin'), ('Edinburgh', 'Edinburgh'), ('Florence', 'Florence'), ('Geneva', 'Geneva'), ('Helsinki', 'Helsinki'), ('Istanbul', 'Istanbul'), ('Lisbon', 'Lisbon'), ('London', 'London'), ('Lucerne', 'Lucerne'), ('Madrid', 'Madrid'), ('Milan', 'Milan'), ('Moscow', 'Moscow'), ('Munich', 'Munich'), ('Naples', 'Naples'), ('Nice', 'Nice'), ('Oslo', 'Oslo'), ('Paris', 'Paris'), ('Prague', 'Prague'), ('Pisa', 'Pisa'), ('Reykjavik', 'Reykjavik'), ('Rome', 'Rome'), ('Salzburg', 'Salzburg'), ('Santorini', 'Santorini'), ('Seville', 'Seville'), ('Sofia', 'Sofia'), ('Split', 'Split'), ('Stockholm', 'Stockholm'), ('Varna', 'Varna'), ('Venice', 'Venice'), ('Vienna', 'Vienna'), ('Warsaw', 'Warsaw'), ('Zagreb', 'Zagreb'), ('Zurich', 'Zurich')], max_length=318),
        ),
        migrations.AlterField(
            model_name='triprequests',
            name='kind_of_group',
            field=models.CharField(blank=True, choices=[('cultural_sightseeing', 'Cultural Group - Sightseeing'), ('schools_youth', 'Schools, Students or Youth'), ('backpackers', 'Backpackers'), ('theme_parks', 'Theme Parks (Eurodisney, Pinocchio, Mirabilandia, Puerto Aventura, Harry Potter...)'), ('study_language', 'Study or Language Package'), ('festivals_events', 'Festivals or Events'), ('sport', 'Sport'), ('family', 'Family'), ('religious', 'Religious'), ('relax_health_spas', 'Relax, Health, and SPAs'), ('adventure_nature', 'Adventure, Nature, Eco-tourism'), ('foodies_gastro_wine', 'Foodies - Gastro Tours - Wine Tours'), ('shopping', 'Shopping Tours'), ('yoga_meditation', 'Yoga or Meditation'), ('theme_tour', 'Theme Tour (Urban Art, Architecture, Science, Cinema...)'), ('photo_tours', 'Photo Tours'), ('cruises', 'Cruises')], max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='triprequests',
            name='meals',
            field=models.CharField(blank=True, choices=[('no meals included', 'No meals included'), ('breakfast only (BB)', 'Breakfast Only (BB)'), ('breakfast & dinner (HB)', 'Breakfast & Dinner (HB)'), ('breakfast, lunch & dinner (FB)', 'Breakfast, Lunch & Dinner (FB)')], max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='triprequests',
            name='meals_details',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='triprequests',
            name='staff',
            field=models.CharField(blank=True, choices=[('Tour leader during the entire trip', 'Tour leader during the entire trip'), ('Official tourist guides in each city', 'Official Tourist Guides')], max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='triprequests',
            name='transportation_details',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='triprequests',
            name='trip_duration',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='triprequests',
            name='type_of_trip',
            field=models.TextField(blank=True, null=True),
        ),
    ]
