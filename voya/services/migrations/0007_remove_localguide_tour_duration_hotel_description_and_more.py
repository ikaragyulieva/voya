# Generated by Django 5.1.2 on 2025-02-12 19:27

import django.db.models.deletion
import phonenumber_field.modelfields
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0006_hotel_telephone_number_localguide_telephone_number_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='localguide',
            name='tour_duration',
        ),
        migrations.AddField(
            model_name='hotel',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='hotel',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
        migrations.AddField(
            model_name='hotel',
            name='street_address',
            field=models.CharField(default='a', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='hotel',
            name='website',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='hotel',
            name='zone',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='hotel',
            name='zone_description',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='localguide',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='localguide',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
        migrations.AddField(
            model_name='localguide',
            name='label',
            field=models.CharField(default='a', max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='localguide',
            name='tour_description',
            field=models.TextField(default='a'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='localguide',
            name='website',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='privatetransport',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='privatetransport',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
        migrations.AddField(
            model_name='privatetransport',
            name='website',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='publictransport',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='publictransport',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
        migrations.AddField(
            model_name='publictransport',
            name='website',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='ticket',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
        migrations.AddField(
            model_name='ticket',
            name='type',
            field=models.CharField(choices=[('choice', 'Select'), ('ticket', 'Ticket'), ('pack', 'Package'), ('other', 'Other')], default='choice', max_length=20),
        ),
        migrations.AddField(
            model_name='ticket',
            name='website',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='transfer',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='transfer',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
        migrations.AddField(
            model_name='transfer',
            name='website',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='hotel',
            name='city',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='hotel',
            name='telephone_number',
            field=phonenumber_field.modelfields.PhoneNumberField(blank=True, help_text='Enter phone number in international format. Example: +123456789', max_length=128, null=True, region=None),
        ),
        migrations.AlterField(
            model_name='localguide',
            name='telephone_number',
            field=phonenumber_field.modelfields.PhoneNumberField(blank=True, help_text='Enter phone number in international format. Example: +123456789', max_length=128, null=True, region=None),
        ),
        migrations.AlterField(
            model_name='privatetransport',
            name='telephone_number',
            field=phonenumber_field.modelfields.PhoneNumberField(blank=True, help_text='Enter phone number in international format. Example: +123456789', max_length=128, null=True, region=None),
        ),
        migrations.AlterField(
            model_name='privatetransport',
            name='type',
            field=models.CharField(choices=[('pr transp', 'Select an option'), ('private bus', 'Private bus'), ('private car', 'Private car'), ('private van', 'Private van'), ('private boat', 'Private boat'), ('other', 'Other')], default='pr transp', max_length=30),
        ),
        migrations.AlterField(
            model_name='publictransport',
            name='telephone_number',
            field=phonenumber_field.modelfields.PhoneNumberField(blank=True, help_text='Enter phone number in international format. Example: +123456789', max_length=128, null=True, region=None),
        ),
        migrations.AlterField(
            model_name='publictransport',
            name='type',
            field=models.CharField(choices=[('pub transp', 'Select an option'), ('public bus', 'Public Bus'), ('train', 'Train'), ('flights', 'Flights'), ('ferry', 'Ferry'), ('metro', 'Metro'), ('other', 'Other')], default='pub transp', max_length=30),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='telephone_number',
            field=phonenumber_field.modelfields.PhoneNumberField(blank=True, help_text='Enter phone number in international format. Example: +123456789', max_length=128, null=True, region=None),
        ),
        migrations.AlterField(
            model_name='transfer',
            name='telephone_number',
            field=phonenumber_field.modelfields.PhoneNumberField(blank=True, help_text='Enter phone number in international format. Example: +123456789', max_length=128, null=True, region=None),
        ),
        migrations.CreateModel(
            name='Staff',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('country', models.CharField(choices=[('cc', 'Select country'), ('AL', 'Albania'), ('AD', 'Andorra'), ('AM', 'Armenia'), ('AT', 'Austria'), ('AZ', 'Azerbaijan'), ('BY', 'Belarus'), ('BE', 'Belgium'), ('BA', 'Bosnia and Herzegovina'), ('BG', 'Bulgaria'), ('HR', 'Croatia'), ('CY', 'Cyprus'), ('CZ', 'Czech Republic'), ('DK', 'Denmark'), ('EE', 'Estonia'), ('FI', 'Finland'), ('FR', 'France'), ('GE', 'Georgia'), ('DE', 'Germany'), ('GR', 'Greece'), ('HU', 'Hungary'), ('IS', 'Iceland'), ('IE', 'Ireland'), ('IT', 'Italy'), ('XK', 'Kosovo'), ('LV', 'Latvia'), ('LI', 'Liechtenstein'), ('LT', 'Lithuania'), ('LU', 'Luxembourg'), ('MT', 'Malta'), ('MD', 'Moldova'), ('MC', 'Monaco'), ('ME', 'Montenegro'), ('NL', 'Netherlands'), ('MK', 'North Macedonia'), ('NO', 'Norway'), ('PL', 'Poland'), ('PT', 'Portugal'), ('RO', 'Romania'), ('SM', 'San Marino'), ('RS', 'Serbia'), ('SK', 'Slovakia'), ('SI', 'Slovenia'), ('ES', 'Spain'), ('SE', 'Sweden'), ('CH', 'Switzerland'), ('TR', 'Turkey'), ('UA', 'Ukraine'), ('GB', 'United Kingdom'), ('VA', 'Vatican City'), ('DZ', 'Algeria'), ('EG', 'Egypt'), ('IL', 'Israel'), ('LB', 'Lebanon'), ('LY', 'Libya'), ('MA', 'Morocco'), ('PS', 'Palestine'), ('SY', 'Syria'), ('TN', 'Tunisia')], default='cc', max_length=100)),
                ('city', models.CharField(choices=[('Select city', 'Select city'), ('Amsterdam', 'Amsterdam'), ('Athens', 'Athens'), ('Barcelona', 'Barcelona'), ('Belgrade', 'Belgrade'), ('Berlin', 'Berlin'), ('Bruges', 'Bruges'), ('Brussels', 'Brussels'), ('Budapest', 'Budapest'), ('Copenhagen', 'Copenhagen'), ('Dublin', 'Dublin'), ('Edinburgh', 'Edinburgh'), ('Florence', 'Florence'), ('Geneva', 'Geneva'), ('Helsinki', 'Helsinki'), ('Istanbul', 'Istanbul'), ('Lisbon', 'Lisbon'), ('London', 'London'), ('Lucerne', 'Lucerne'), ('Madrid', 'Madrid'), ('Milan', 'Milan'), ('Moscow', 'Moscow'), ('Munich', 'Munich'), ('Naples', 'Naples'), ('Nice', 'Nice'), ('Oslo', 'Oslo'), ('Paris', 'Paris'), ('Prague', 'Prague'), ('Pisa', 'Pisa'), ('Reykjavik', 'Reykjavik'), ('Rome', 'Rome'), ('Salzburg', 'Salzburg'), ('Santorini', 'Santorini'), ('Seville', 'Seville'), ('Sofia', 'Sofia'), ('Split', 'Split'), ('Stockholm', 'Stockholm'), ('Varna', 'Varna'), ('Venice', 'Venice'), ('Vienna', 'Vienna'), ('Warsaw', 'Warsaw'), ('Zagreb', 'Zagreb'), ('Zurich', 'Zurich')], default='Select city', max_length=50)),
                ('capacity', models.IntegerField(default=1)),
                ('telephone_number', phonenumber_field.modelfields.PhoneNumberField(blank=True, help_text='Enter phone number in international format. Example: +123456789', max_length=128, null=True, region=None)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('website', models.URLField(blank=True, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('name', models.CharField(max_length=80)),
                ('mansion', models.CharField(max_length=50)),
                ('price', models.DecimalField(decimal_places=2, max_digits=5)),
                ('price_includes', models.CharField(max_length=200)),
                ('tour_description', models.TextField()),
                ('label', models.CharField(max_length=50)),
                ('created_by_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_created_by', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
