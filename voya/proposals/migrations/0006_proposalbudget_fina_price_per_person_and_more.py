# Generated by Django 5.1.2 on 2024-12-04 12:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proposals', '0005_proposalsectionitem_price_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='proposalbudget',
            name='fina_price_per_person',
            field=models.DecimalField(decimal_places=2, default=1.0, max_digits=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='proposalbudget',
            name='final_price',
            field=models.DecimalField(decimal_places=2, default=1.0, max_digits=10),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='proposalbudget',
            name='fixed_cost',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name='proposalbudget',
            name='service_fee',
            field=models.DecimalField(decimal_places=2, default=500.0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='proposalbudget',
            name='total_cost',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name='proposalbudget',
            name='total_cost_per_person',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name='proposalbudget',
            name='variable_cost',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
    ]