# Generated by Django 3.1.5 on 2021-04-03 22:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('season', '0041_auto_20210403_2153'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='teamprofile',
            options={'ordering': ('-points_total',)},
        ),
    ]
