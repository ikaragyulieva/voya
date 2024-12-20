# Generated by Django 5.1.2 on 2024-11-24 19:35

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('proposals', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='proposalsectionitem',
            name='content_type',
        ),
        migrations.RemoveField(
            model_name='proposalsectionitem',
            name='object_id',
        ),
        migrations.RemoveField(
            model_name='proposalsectionitem',
            name='order',
        ),
        migrations.AddField(
            model_name='proposalsectionitem',
            name='corresponding_trip_date',
            field=models.DateField(default='2024-11-23'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='proposalsectionitem',
            name='proposal',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='proposals.proposal'),
        ),
        migrations.CreateModel(
            name='ServiceLink',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_id', models.PositiveIntegerField()),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype')),
            ],
            options={
                'unique_together': {('content_type', 'object_id')},
            },
        ),
        migrations.AddField(
            model_name='proposalsectionitem',
            name='services',
            field=models.ManyToManyField(related_name='item_service', to='proposals.servicelink'),
        ),
    ]
