# Generated by Django 3.1.5 on 2021-05-26 11:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('season', '0049_event_tla'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='round',
            field=models.IntegerField(default=0),
        ),
    ]