# Generated by Django 3.1.5 on 2021-02-10 13:15

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('season', '0022_auto_20210210_1205'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='result',
            name='eventType',
        ),
        migrations.RemoveField(
            model_name='scoringevent',
            name='endDateTime',
        ),
        migrations.RemoveField(
            model_name='scoringevent',
            name='startDateTime',
        ),
        migrations.AddField(
            model_name='event',
            name='endDateTime',
            field=models.DateTimeField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='event',
            name='startDateTime',
            field=models.DateTimeField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='result',
            name='raceTime',
            field=models.IntegerField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='scoringevent',
            name='event_ID',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='season.event'),
        ),
    ]
