# Generated by Django 3.1.5 on 2021-03-11 14:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('season', '0023_auto_20210310_1758'),
    ]

    operations = [
        migrations.AddField(
            model_name='competitorscore',
            name='scoringevent_ID',
            field=models.IntegerField(default=0),
        ),
    ]
