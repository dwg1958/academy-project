# Generated by Django 3.1.5 on 2021-02-17 17:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('season', '0010_remove_result_pole'),
    ]

    operations = [
        migrations.AlterField(
            model_name='result',
            name='competitor_ID',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='competitor', to='season.competitor'),
        ),
    ]
