# Generated by Django 3.1.5 on 2021-03-13 13:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('season', '0027_auto_20210311_1539'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teamprofile',
            name='p1_1',
            field=models.ForeignKey(default=1, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='p1_1', to='season.competitor'),
        ),
        migrations.AlterField(
            model_name='teamprofile',
            name='p1_2',
            field=models.ForeignKey(default=1, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='p1_2', to='season.competitor'),
        ),
        migrations.AlterField(
            model_name='teamprofile',
            name='p2_1',
            field=models.ForeignKey(default=1, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='p2_1', to='season.competitor'),
        ),
        migrations.AlterField(
            model_name='teamprofile',
            name='p2_2',
            field=models.ForeignKey(default=1, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='p2_2', to='season.competitor'),
        ),
        migrations.AlterField(
            model_name='teamprofile',
            name='p3_1',
            field=models.ForeignKey(default=1, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='p3_1', to='season.competitor'),
        ),
        migrations.AlterField(
            model_name='teamprofile',
            name='p3_2',
            field=models.ForeignKey(default=1, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='p3_2', to='season.competitor'),
        ),
        migrations.AlterField(
            model_name='teamprofile',
            name='pw_1',
            field=models.ForeignKey(default=1, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='pw_1', to='season.competitor'),
        ),
        migrations.AlterField(
            model_name='teamprofile',
            name='pw_2',
            field=models.ForeignKey(default=1, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='pw_2', to='season.competitor'),
        ),
    ]
