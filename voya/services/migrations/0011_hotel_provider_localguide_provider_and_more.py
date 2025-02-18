# Generated by Django 5.1.2 on 2025-02-18 22:21

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('providers', '0003_alter_providers_commercial_name'),
        ('services', '0010_rename_guide_name_localguide_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='hotel',
            name='provider',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_provider', to='providers.providers'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='localguide',
            name='provider',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_provider', to='providers.providers'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='privatetransport',
            name='provider',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_provider', to='providers.providers'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='publictransport',
            name='provider',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_provider', to='providers.providers'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='staff',
            name='provider',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_provider', to='providers.providers'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='ticket',
            name='provider',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_provider', to='providers.providers'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='transfer',
            name='provider',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_provider', to='providers.providers'),
            preserve_default=False,
        ),
    ]
