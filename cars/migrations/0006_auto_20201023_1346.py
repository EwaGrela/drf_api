# Generated by Django 3.1.2 on 2020-10-23 11:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cars', '0005_auto_20201023_1215'),
    ]

    operations = [
        migrations.AlterField(
            model_name='car',
            name='rating',
            field=models.IntegerField(default=0),
        ),
    ]