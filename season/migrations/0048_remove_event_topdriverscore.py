# Generated by Django 3.1.5 on 2021-05-14 11:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('season', '0047_auto_20210514_1121'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='topDriverScore',
        ),
    ]
