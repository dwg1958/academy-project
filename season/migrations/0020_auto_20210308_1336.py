# Generated by Django 3.1.5 on 2021-03-08 13:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('season', '0019_auto_20210307_1343'),
    ]

    operations = [
        migrations.CreateModel(
            name='CompetitorScore',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pointsType', models.CharField(choices=[('P', 'Position'), ('F', 'Fastest Lap'), ('G', 'Places Gained / Lost'), ('L', 'Laps Behind Leader'), ('D', 'Disqualification')], max_length=1)),
                ('t1_score', models.DecimalField(decimal_places=2, max_digits=6)),
                ('t2_score', models.DecimalField(decimal_places=2, max_digits=6)),
                ('result_ID', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='result', to='season.result')),
            ],
        ),
        migrations.CreateModel(
            name='TeamScore',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('teamPosition', models.CharField(choices=[('1', '1. Lead Driver'), ('2', '2. Second Driver')], max_length=1)),
                ('pointsType', models.CharField(choices=[('P', 'Position'), ('F', 'Fastest Lap'), ('G', 'Places Gained / Lost'), ('L', 'Laps Behind Leader'), ('D', 'Disqualification')], max_length=1)),
                ('academyPoints', models.DecimalField(decimal_places=2, max_digits=6)),
                ('cscore_ID', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='cscore', to='season.result')),
                ('team_ID', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='team', to='season.teamprofile')),
            ],
        ),
        migrations.RemoveField(
            model_name='teammember',
            name='competitor_ID',
        ),
        migrations.RemoveField(
            model_name='teammember',
            name='team_ID',
        ),
        migrations.RemoveField(
            model_name='academyscoringmatrix',
            name='multiplier',
        ),
        migrations.RemoveField(
            model_name='academyscoringmatrix',
            name='pointsType',
        ),
        migrations.RemoveField(
            model_name='academyscoringmatrix',
            name='role',
        ),
        migrations.AddField(
            model_name='academyscoringmatrix',
            name='m_1',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=6),
        ),
        migrations.AddField(
            model_name='academyscoringmatrix',
            name='m_10',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=6),
        ),
        migrations.AddField(
            model_name='academyscoringmatrix',
            name='m_2',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=6),
        ),
        migrations.AddField(
            model_name='academyscoringmatrix',
            name='m_3',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=6),
        ),
        migrations.AddField(
            model_name='academyscoringmatrix',
            name='m_4',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=6),
        ),
        migrations.AddField(
            model_name='academyscoringmatrix',
            name='m_5',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=6),
        ),
        migrations.AddField(
            model_name='academyscoringmatrix',
            name='m_6',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=6),
        ),
        migrations.AddField(
            model_name='academyscoringmatrix',
            name='m_7',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=6),
        ),
        migrations.AddField(
            model_name='academyscoringmatrix',
            name='m_8',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=6),
        ),
        migrations.AddField(
            model_name='academyscoringmatrix',
            name='m_9',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=6),
        ),
        migrations.AddField(
            model_name='academyscoringmatrix',
            name='m_disqualified',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=6),
        ),
        migrations.AddField(
            model_name='academyscoringmatrix',
            name='m_fastest_lap',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=6),
        ),
        migrations.AddField(
            model_name='academyscoringmatrix',
            name='m_laps_off_leader',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=6),
        ),
        migrations.AddField(
            model_name='academyscoringmatrix',
            name='m_pos_gained',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=6),
        ),
        migrations.AddField(
            model_name='academyscoringmatrix',
            name='q_1',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=6),
        ),
        migrations.AddField(
            model_name='academyscoringmatrix',
            name='q_10',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=6),
        ),
        migrations.AddField(
            model_name='academyscoringmatrix',
            name='q_2',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=6),
        ),
        migrations.AddField(
            model_name='academyscoringmatrix',
            name='q_3',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=6),
        ),
        migrations.AddField(
            model_name='academyscoringmatrix',
            name='q_4',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=6),
        ),
        migrations.AddField(
            model_name='academyscoringmatrix',
            name='q_5',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=6),
        ),
        migrations.AddField(
            model_name='academyscoringmatrix',
            name='q_6',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=6),
        ),
        migrations.AddField(
            model_name='academyscoringmatrix',
            name='q_7',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=6),
        ),
        migrations.AddField(
            model_name='academyscoringmatrix',
            name='q_8',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=6),
        ),
        migrations.AddField(
            model_name='academyscoringmatrix',
            name='q_9',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=6),
        ),
        migrations.AddField(
            model_name='academyscoringmatrix',
            name='s_1',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=6),
        ),
        migrations.AddField(
            model_name='academyscoringmatrix',
            name='s_10',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=6),
        ),
        migrations.AddField(
            model_name='academyscoringmatrix',
            name='s_2',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=6),
        ),
        migrations.AddField(
            model_name='academyscoringmatrix',
            name='s_3',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=6),
        ),
        migrations.AddField(
            model_name='academyscoringmatrix',
            name='s_4',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=6),
        ),
        migrations.AddField(
            model_name='academyscoringmatrix',
            name='s_5',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=6),
        ),
        migrations.AddField(
            model_name='academyscoringmatrix',
            name='s_6',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=6),
        ),
        migrations.AddField(
            model_name='academyscoringmatrix',
            name='s_7',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=6),
        ),
        migrations.AddField(
            model_name='academyscoringmatrix',
            name='s_8',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=6),
        ),
        migrations.AddField(
            model_name='academyscoringmatrix',
            name='s_9',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=6),
        ),
        migrations.AddField(
            model_name='academyscoringmatrix',
            name='s_disqualified',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=6),
        ),
        migrations.AddField(
            model_name='academyscoringmatrix',
            name='s_fastest_lap',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=6),
        ),
        migrations.AddField(
            model_name='academyscoringmatrix',
            name='s_laps_off_leader',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=6),
        ),
        migrations.AddField(
            model_name='academyscoringmatrix',
            name='s_pos_gained',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=6),
        ),
        migrations.AddField(
            model_name='academyscoringmatrix',
            name='teamPosition',
            field=models.CharField(choices=[('1', '1. Lead Driver'), ('2', '2. Second Driver')], default='1', max_length=1),
        ),
        migrations.DeleteModel(
            name='ScoringMatches',
        ),
        migrations.DeleteModel(
            name='TeamMember',
        ),
    ]
