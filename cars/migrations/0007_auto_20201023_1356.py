# Generated by Django 3.1.2 on 2020-10-23 11:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cars', '0006_auto_20201023_1346'),
    ]

    operations = [
        migrations.RenameField(
            model_name='car',
            old_name='rating',
            new_name='average_rate',
        ),
        migrations.AddField(
            model_name='car',
            name='sum_rates',
            field=models.IntegerField(default=0),
        ),
    ]
