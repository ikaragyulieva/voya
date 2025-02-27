# Generated by Django 5.1.2 on 2025-02-25 17:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('providers', '0003_alter_providers_commercial_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='providers',
            name='city',
            field=models.CharField(choices=[('', 'Select a city'), ('Amsterdam', 'Amsterdam'), ('Athens', 'Athens'), ('Barcelona', 'Barcelona'), ('Belgrade', 'Belgrade'), ('Berlin', 'Berlin'), ('Bordeaux', 'Bordeaux'), ('Bruges', 'Bruges'), ('Brussels', 'Brussels'), ('Budapest', 'Budapest'), ('Cappadocia', 'Cappadocia'), ('Capri', 'Capri'), ('Chamonix', 'Chamonix'), ('Colmar', 'Colmar'), ('Como', 'Como'), ('Copenhagen', 'Copenhagen'), ('Dublin', 'Dublin'), ('Dubrovnik', 'Dubrovnik'), ('Edinburgh', 'Edinburgh'), ('Florence', 'Florence'), ('Frankfurth', 'Frankfurth'), ('Geneva', 'Geneva'), ('Ghent', 'Ghent'), ('Helsinki', 'Helsinki'), ('Hvar', 'Hvar'), ('Ibiza', 'Ibiza'), ('Istanbul', 'Istanbul'), ('Lisbon', 'Lisbon'), ('Loire', 'Loire'), ('London', 'London'), ('Lucerne', 'Lucerne'), ('Madrid', 'Madrid'), ('Milan', 'Milan'), ('Montecatini Terme', 'Montecatini Terme'), ('Moscow', 'Moscow'), ('Munich', 'Munich'), ('Mykonos', 'Mykonos'), ('Naples', 'Naples'), ('Nice', 'Nice'), ('Oporto', 'Oporto'), ('Oslo', 'Oslo'), ('Pamplona', 'Pamplona'), ('Paris', 'Paris'), ('Prague', 'Prague'), ('Pisa', 'Pisa'), ('Reykjavik', 'Reykjavik'), ('Rome', 'Rome'), ('Salzburg', 'Salzburg'), ('Santiago de Compostela', 'Santiago de Compostela'), ('Santorini', 'Santorini'), ('Seville', 'Seville'), ('Sofia', 'Sofia'), ('Split', 'Split'), ('Stockholm', 'Stockholm'), ('Varna', 'Varna'), ('Venice', 'Venice'), ('Vienna', 'Vienna'), ('Warsaw', 'Warsaw'), ('Zagreb', 'Zagreb'), ('Zaragoza', 'Zaragoza'), ('Zurich', 'Zurich')], default='Select city', max_length=50),
        ),
    ]
