# Generated by Django 3.1.5 on 2021-04-03 21:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('season', '0040_auto_20210325_1337'),
    ]

    operations = [
        migrations.AddField(
            model_name='teamprofile',
            name='position_f1',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='teamprofile',
            name='position_f2',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='teamprofile',
            name='position_f3',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='teamprofile',
            name='position_ws',
            field=models.IntegerField(default=0),
        ),
    ]
