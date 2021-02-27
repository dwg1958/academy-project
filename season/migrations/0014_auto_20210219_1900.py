# Generated by Django 3.1.5 on 2021-02-19 19:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('season', '0013_auto_20210219_1125'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='circuit',
            field=models.CharField(max_length=30),
        ),
        migrations.AlterField(
            model_name='event',
            name='formulas',
            field=models.CharField(max_length=45),
        ),
        migrations.AlterField(
            model_name='event',
            name='name',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='result',
            name='competitor_ID',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='competitor', to='season.competitor'),
        ),
        migrations.AlterField(
            model_name='teamprofile',
            name='teamName',
            field=models.CharField(default='My Team', max_length=30),
        ),
        migrations.CreateModel(
            name='TeamMember',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', models.CharField(choices=[('1_1', 'F1 Lead Driver'), ('1_2', 'F1 Second Driver'), ('1_M', 'F1 Manager'), ('2_1', 'F2 Lead Driver'), ('2_2', 'F2 Second Driver'), ('2_M', 'F2 Manager'), ('3_1', 'F3 Lead Driver'), ('3_2', 'F3 Second Driver'), ('3_M', 'F3 Manager'), ('W_1', 'W Lead Driver'), ('W_2', 'W Second Driver'), ('W_M', 'W Manager')], max_length=3)),
                ('dateSelected', models.DateTimeField(auto_now=True)),
                ('competitor_ID', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='member', to='season.competitor')),
                ('team_ID', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='team', to='season.teamprofile')),
            ],
        ),
    ]