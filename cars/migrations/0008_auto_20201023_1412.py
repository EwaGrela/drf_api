# Generated by Django 3.1.2 on 2020-10-23 12:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cars', '0007_auto_20201023_1356'),
    ]

    operations = [
        migrations.AlterField(
            model_name='car',
            name='average_rate',
            field=models.FloatField(default=0),
        ),
    ]