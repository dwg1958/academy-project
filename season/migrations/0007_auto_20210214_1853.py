# Generated by Django 3.1.5 on 2021-02-14 18:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('season', '0006_auto_20210213_1814'),
    ]

    operations = [
        migrations.AlterField(
            model_name='result',
            name='scoringEvent_ID',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='result', to='season.scoringevent'),
        ),
        migrations.AlterField(
            model_name='scoringevent',
            name='event_ID',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='scoringEvent', to='season.event'),
        ),
        migrations.AlterField(
            model_name='scoringmatches',
            name='player_ID',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='player', to='season.teamprofile'),
        ),
        migrations.AlterField(
            model_name='scoringmatches',
            name='result_ID',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='result', to='season.result'),
        ),
        migrations.AlterField(
            model_name='teamprofile',
            name='dateStarted',
            field=models.DateField(auto_now=True),
        ),
    ]
