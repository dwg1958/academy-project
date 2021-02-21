# Generated by Django 3.1.5 on 2021-02-19 11:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('season', '0012_auto_20210218_1828'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='result',
            options={'ordering': ('scoringEvent_ID',)},
        ),
        migrations.AlterModelOptions(
            name='scoringevent',
            options={'ordering': ('formula', 'startDateTime')},
        ),
        migrations.AlterField(
            model_name='result',
            name='competitor_ID',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='competitor', to='season.competitor'),
        ),
        migrations.AlterField(
            model_name='result',
            name='scoringEvent_ID',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='result', to='season.scoringevent'),
        ),
        migrations.AlterField(
            model_name='scoringevent',
            name='event_ID',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='scoringEvent', to='season.event'),
        ),
        migrations.AlterField(
            model_name='scoringmatches',
            name='player_ID',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='player', to='season.teamprofile'),
        ),
        migrations.AlterField(
            model_name='scoringmatches',
            name='result_ID',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='result', to='season.result'),
        ),
    ]
