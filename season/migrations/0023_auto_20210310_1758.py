# Generated by Django 3.1.5 on 2021-03-10 17:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('season', '0022_academyscoringmatrix_q_disqualified'),
    ]

    operations = [
        migrations.RenameField(
            model_name='result',
            old_name='lapsComplete',
            new_name='laps_off_leader',
        ),
    ]
