# Generated by Django 5.1.2 on 2024-11-11 12:36

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0004_remove_companyprofile_country_and_more'),
        ('requests', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='triprequests',
            name='created_by_company',
            field=models.ForeignKey(default=0.0004938271604938272, on_delete=django.db.models.deletion.CASCADE, related_name='request_company', to='companies.companyprofile'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='triprequests',
            name='created_by_user',
            field=models.ForeignKey(default=0.0004938271604938272, on_delete=django.db.models.deletion.CASCADE, related_name='request_user', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='triprequests',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='triprequests',
            name='age_range',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='triprequests',
            name='city_destinations',
            field=models.CharField(choices=[('Amsterdam', 'Amsterdam'), ('Athens', 'Athens'), ('Barcelona', 'Barcelona'), ('Belgrade', 'Belgrade'), ('Berlin', 'Berlin'), ('Bruges', 'Bruges'), ('Brussels', 'Brussels'), ('Budapest', 'Budapest'), ('Copenhagen', 'Copenhagen'), ('Dublin', 'Dublin'), ('Edinburgh', 'Edinburgh'), ('Florence', 'Florence'), ('Geneva', 'Geneva'), ('Helsinki', 'Helsinki'), ('Istanbul', 'Istanbul'), ('Lisbon', 'Lisbon'), ('London', 'London'), ('Lucerne', 'Lucerne'), ('Madrid', 'Madrid'), ('Milan', 'Milan'), ('Moscow', 'Moscow'), ('Munich', 'Munich'), ('Naples', 'Naples'), ('Nice', 'Nice'), ('Oslo', 'Oslo'), ('Paris', 'Paris'), ('Prague', 'Prague'), ('Pisa', 'Pisa'), ('Reykjavik', 'Reykjavik'), ('Rome', 'Rome'), ('Salzburg', 'Salzburg'), ('Santorini', 'Santorini'), ('Seville', 'Seville'), ('Sofia', 'Sofia'), ('Split', 'Split'), ('Stockholm', 'Stockholm'), ('Varna', 'Varna'), ('Venice', 'Venice'), ('Vienna', 'Vienna'), ('Warsaw', 'Warsaw'), ('Zagreb', 'Zagreb'), ('Zurich', 'Zurich')], max_length=250),
        ),
        migrations.AlterField(
            model_name='triprequests',
            name='country_destinations',
            field=models.TextField(help_text='Choose the countries you would like to visit'),
        ),
        migrations.AlterField(
            model_name='triprequests',
            name='trip_duration',
            field=models.PositiveIntegerField(),
        ),
    ]
