# Generated by Django 5.1.2 on 2024-12-05 08:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0003_rename_bus_price_airport_transfers_price_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hotels',
            name='city',
            field=models.CharField(choices=[('Select city', 'Select city'), ('Amsterdam', 'Amsterdam'), ('Athens', 'Athens'), ('Barcelona', 'Barcelona'), ('Belgrade', 'Belgrade'), ('Berlin', 'Berlin'), ('Bruges', 'Bruges'), ('Brussels', 'Brussels'), ('Budapest', 'Budapest'), ('Copenhagen', 'Copenhagen'), ('Dublin', 'Dublin'), ('Edinburgh', 'Edinburgh'), ('Florence', 'Florence'), ('Geneva', 'Geneva'), ('Helsinki', 'Helsinki'), ('Istanbul', 'Istanbul'), ('Lisbon', 'Lisbon'), ('London', 'London'), ('Lucerne', 'Lucerne'), ('Madrid', 'Madrid'), ('Milan', 'Milan'), ('Moscow', 'Moscow'), ('Munich', 'Munich'), ('Naples', 'Naples'), ('Nice', 'Nice'), ('Oslo', 'Oslo'), ('Paris', 'Paris'), ('Prague', 'Prague'), ('Pisa', 'Pisa'), ('Reykjavik', 'Reykjavik'), ('Rome', 'Rome'), ('Salzburg', 'Salzburg'), ('Santorini', 'Santorini'), ('Seville', 'Seville'), ('Sofia', 'Sofia'), ('Split', 'Split'), ('Stockholm', 'Stockholm'), ('Varna', 'Varna'), ('Venice', 'Venice'), ('Vienna', 'Vienna'), ('Warsaw', 'Warsaw'), ('Zagreb', 'Zagreb'), ('Zurich', 'Zurich')], max_length=50),
        ),
        migrations.AlterField(
            model_name='localguides',
            name='city',
            field=models.CharField(choices=[('Select city', 'Select city'), ('Amsterdam', 'Amsterdam'), ('Athens', 'Athens'), ('Barcelona', 'Barcelona'), ('Belgrade', 'Belgrade'), ('Berlin', 'Berlin'), ('Bruges', 'Bruges'), ('Brussels', 'Brussels'), ('Budapest', 'Budapest'), ('Copenhagen', 'Copenhagen'), ('Dublin', 'Dublin'), ('Edinburgh', 'Edinburgh'), ('Florence', 'Florence'), ('Geneva', 'Geneva'), ('Helsinki', 'Helsinki'), ('Istanbul', 'Istanbul'), ('Lisbon', 'Lisbon'), ('London', 'London'), ('Lucerne', 'Lucerne'), ('Madrid', 'Madrid'), ('Milan', 'Milan'), ('Moscow', 'Moscow'), ('Munich', 'Munich'), ('Naples', 'Naples'), ('Nice', 'Nice'), ('Oslo', 'Oslo'), ('Paris', 'Paris'), ('Prague', 'Prague'), ('Pisa', 'Pisa'), ('Reykjavik', 'Reykjavik'), ('Rome', 'Rome'), ('Salzburg', 'Salzburg'), ('Santorini', 'Santorini'), ('Seville', 'Seville'), ('Sofia', 'Sofia'), ('Split', 'Split'), ('Stockholm', 'Stockholm'), ('Varna', 'Varna'), ('Venice', 'Venice'), ('Vienna', 'Vienna'), ('Warsaw', 'Warsaw'), ('Zagreb', 'Zagreb'), ('Zurich', 'Zurich')], max_length=50),
        ),
        migrations.AlterField(
            model_name='privatetransport',
            name='city',
            field=models.CharField(choices=[('Select city', 'Select city'), ('Amsterdam', 'Amsterdam'), ('Athens', 'Athens'), ('Barcelona', 'Barcelona'), ('Belgrade', 'Belgrade'), ('Berlin', 'Berlin'), ('Bruges', 'Bruges'), ('Brussels', 'Brussels'), ('Budapest', 'Budapest'), ('Copenhagen', 'Copenhagen'), ('Dublin', 'Dublin'), ('Edinburgh', 'Edinburgh'), ('Florence', 'Florence'), ('Geneva', 'Geneva'), ('Helsinki', 'Helsinki'), ('Istanbul', 'Istanbul'), ('Lisbon', 'Lisbon'), ('London', 'London'), ('Lucerne', 'Lucerne'), ('Madrid', 'Madrid'), ('Milan', 'Milan'), ('Moscow', 'Moscow'), ('Munich', 'Munich'), ('Naples', 'Naples'), ('Nice', 'Nice'), ('Oslo', 'Oslo'), ('Paris', 'Paris'), ('Prague', 'Prague'), ('Pisa', 'Pisa'), ('Reykjavik', 'Reykjavik'), ('Rome', 'Rome'), ('Salzburg', 'Salzburg'), ('Santorini', 'Santorini'), ('Seville', 'Seville'), ('Sofia', 'Sofia'), ('Split', 'Split'), ('Stockholm', 'Stockholm'), ('Varna', 'Varna'), ('Venice', 'Venice'), ('Vienna', 'Vienna'), ('Warsaw', 'Warsaw'), ('Zagreb', 'Zagreb'), ('Zurich', 'Zurich')], max_length=50),
        ),
        migrations.AlterField(
            model_name='publictransport',
            name='city',
            field=models.CharField(choices=[('Select city', 'Select city'), ('Amsterdam', 'Amsterdam'), ('Athens', 'Athens'), ('Barcelona', 'Barcelona'), ('Belgrade', 'Belgrade'), ('Berlin', 'Berlin'), ('Bruges', 'Bruges'), ('Brussels', 'Brussels'), ('Budapest', 'Budapest'), ('Copenhagen', 'Copenhagen'), ('Dublin', 'Dublin'), ('Edinburgh', 'Edinburgh'), ('Florence', 'Florence'), ('Geneva', 'Geneva'), ('Helsinki', 'Helsinki'), ('Istanbul', 'Istanbul'), ('Lisbon', 'Lisbon'), ('London', 'London'), ('Lucerne', 'Lucerne'), ('Madrid', 'Madrid'), ('Milan', 'Milan'), ('Moscow', 'Moscow'), ('Munich', 'Munich'), ('Naples', 'Naples'), ('Nice', 'Nice'), ('Oslo', 'Oslo'), ('Paris', 'Paris'), ('Prague', 'Prague'), ('Pisa', 'Pisa'), ('Reykjavik', 'Reykjavik'), ('Rome', 'Rome'), ('Salzburg', 'Salzburg'), ('Santorini', 'Santorini'), ('Seville', 'Seville'), ('Sofia', 'Sofia'), ('Split', 'Split'), ('Stockholm', 'Stockholm'), ('Varna', 'Varna'), ('Venice', 'Venice'), ('Vienna', 'Vienna'), ('Warsaw', 'Warsaw'), ('Zagreb', 'Zagreb'), ('Zurich', 'Zurich')], max_length=50),
        ),
        migrations.AlterField(
            model_name='tickets',
            name='city',
            field=models.CharField(choices=[('Select city', 'Select city'), ('Amsterdam', 'Amsterdam'), ('Athens', 'Athens'), ('Barcelona', 'Barcelona'), ('Belgrade', 'Belgrade'), ('Berlin', 'Berlin'), ('Bruges', 'Bruges'), ('Brussels', 'Brussels'), ('Budapest', 'Budapest'), ('Copenhagen', 'Copenhagen'), ('Dublin', 'Dublin'), ('Edinburgh', 'Edinburgh'), ('Florence', 'Florence'), ('Geneva', 'Geneva'), ('Helsinki', 'Helsinki'), ('Istanbul', 'Istanbul'), ('Lisbon', 'Lisbon'), ('London', 'London'), ('Lucerne', 'Lucerne'), ('Madrid', 'Madrid'), ('Milan', 'Milan'), ('Moscow', 'Moscow'), ('Munich', 'Munich'), ('Naples', 'Naples'), ('Nice', 'Nice'), ('Oslo', 'Oslo'), ('Paris', 'Paris'), ('Prague', 'Prague'), ('Pisa', 'Pisa'), ('Reykjavik', 'Reykjavik'), ('Rome', 'Rome'), ('Salzburg', 'Salzburg'), ('Santorini', 'Santorini'), ('Seville', 'Seville'), ('Sofia', 'Sofia'), ('Split', 'Split'), ('Stockholm', 'Stockholm'), ('Varna', 'Varna'), ('Venice', 'Venice'), ('Vienna', 'Vienna'), ('Warsaw', 'Warsaw'), ('Zagreb', 'Zagreb'), ('Zurich', 'Zurich')], max_length=50),
        ),
        migrations.AlterField(
            model_name='transfers',
            name='city',
            field=models.CharField(choices=[('Select city', 'Select city'), ('Amsterdam', 'Amsterdam'), ('Athens', 'Athens'), ('Barcelona', 'Barcelona'), ('Belgrade', 'Belgrade'), ('Berlin', 'Berlin'), ('Bruges', 'Bruges'), ('Brussels', 'Brussels'), ('Budapest', 'Budapest'), ('Copenhagen', 'Copenhagen'), ('Dublin', 'Dublin'), ('Edinburgh', 'Edinburgh'), ('Florence', 'Florence'), ('Geneva', 'Geneva'), ('Helsinki', 'Helsinki'), ('Istanbul', 'Istanbul'), ('Lisbon', 'Lisbon'), ('London', 'London'), ('Lucerne', 'Lucerne'), ('Madrid', 'Madrid'), ('Milan', 'Milan'), ('Moscow', 'Moscow'), ('Munich', 'Munich'), ('Naples', 'Naples'), ('Nice', 'Nice'), ('Oslo', 'Oslo'), ('Paris', 'Paris'), ('Prague', 'Prague'), ('Pisa', 'Pisa'), ('Reykjavik', 'Reykjavik'), ('Rome', 'Rome'), ('Salzburg', 'Salzburg'), ('Santorini', 'Santorini'), ('Seville', 'Seville'), ('Sofia', 'Sofia'), ('Split', 'Split'), ('Stockholm', 'Stockholm'), ('Varna', 'Varna'), ('Venice', 'Venice'), ('Vienna', 'Vienna'), ('Warsaw', 'Warsaw'), ('Zagreb', 'Zagreb'), ('Zurich', 'Zurich')], max_length=50),
        ),
    ]
