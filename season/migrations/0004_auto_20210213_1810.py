# Generated by Django 3.1.5 on 2021-02-13 18:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('season', '0003_auto_20210212_1432'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='event',
            options={'ordering': ('-date',)},
        ),
    ]
