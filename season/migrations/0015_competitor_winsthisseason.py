# Generated by Django 3.1.5 on 2021-02-04 14:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('season', '0014_auto_20210204_1405'),
    ]

    operations = [
        migrations.AddField(
            model_name='competitor',
            name='winsThisSeason',
            field=models.IntegerField(default=0),
        ),
    ]
