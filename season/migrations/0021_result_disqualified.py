# Generated by Django 3.1.5 on 2021-03-10 15:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('season', '0020_auto_20210308_1336'),
    ]

    operations = [
        migrations.AddField(
            model_name='result',
            name='disqualified',
            field=models.BooleanField(default=False),
        ),
    ]
