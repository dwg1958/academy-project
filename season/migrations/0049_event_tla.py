# Generated by Django 3.1.5 on 2021-05-24 10:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('season', '0048_remove_event_topdriverscore'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='tla',
            field=models.CharField(default='', max_length=3),
        ),
    ]
