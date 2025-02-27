# Generated by Django 5.1.2 on 2025-02-25 17:40

import multiselectfield.db.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('requests', '0017_alter_triprequests_city_destinations_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='triprequests',
            name='city_destinations',
            field=multiselectfield.db.fields.MultiSelectField(choices=[('', 'Select a city'), ('Amsterdam', 'Amsterdam'), ('Athens', 'Athens'), ('Barcelona', 'Barcelona'), ('Belgrade', 'Belgrade'), ('Berlin', 'Berlin'), ('Bordeaux', 'Bordeaux'), ('Bruges', 'Bruges'), ('Brussels', 'Brussels'), ('Budapest', 'Budapest'), ('Cappadocia', 'Cappadocia'), ('Capri', 'Capri'), ('Chamonix', 'Chamonix'), ('Colmar', 'Colmar'), ('Como', 'Como'), ('Copenhagen', 'Copenhagen'), ('Dublin', 'Dublin'), ('Dubrovnik', 'Dubrovnik'), ('Edinburgh', 'Edinburgh'), ('Florence', 'Florence'), ('Frankfurth', 'Frankfurth'), ('Geneva', 'Geneva'), ('Ghent', 'Ghent'), ('Helsinki', 'Helsinki'), ('Hvar', 'Hvar'), ('Ibiza', 'Ibiza'), ('Istanbul', 'Istanbul'), ('Lisbon', 'Lisbon'), ('Loire', 'Loire'), ('London', 'London'), ('Lucerne', 'Lucerne'), ('Madrid', 'Madrid'), ('Milan', 'Milan'), ('Montecatini Terme', 'Montecatini Terme'), ('Moscow', 'Moscow'), ('Munich', 'Munich'), ('Mykonos', 'Mykonos'), ('Naples', 'Naples'), ('Nice', 'Nice'), ('Oporto', 'Oporto'), ('Oslo', 'Oslo'), ('Pamplona', 'Pamplona'), ('Paris', 'Paris'), ('Prague', 'Prague'), ('Pisa', 'Pisa'), ('Reykjavik', 'Reykjavik'), ('Rome', 'Rome'), ('Salzburg', 'Salzburg'), ('Santiago de Compostela', 'Santiago de Compostela'), ('Santorini', 'Santorini'), ('Seville', 'Seville'), ('Sofia', 'Sofia'), ('Split', 'Split'), ('Stockholm', 'Stockholm'), ('Varna', 'Varna'), ('Venice', 'Venice'), ('Vienna', 'Vienna'), ('Warsaw', 'Warsaw'), ('Zagreb', 'Zagreb'), ('Zaragoza', 'Zaragoza'), ('Zurich', 'Zurich')], max_length=484),
        ),
    ]
