# Generated by Django 5.1.2 on 2024-12-05 14:36

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proposals', '0008_remove_proposalsectionitem_services_and_more'),
        ('requests', '0012_alter_triprequests_city_destinations'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='proposal',
            name='request',
            field=models.ForeignKey(default=15, on_delete=django.db.models.deletion.CASCADE, related_name='request_proposal', to='requests.triprequests'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='proposal',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_proposal', to=settings.AUTH_USER_MODEL),
        ),
    ]
