# Generated by Django 4.0.4 on 2022-10-29 12:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nav', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='buildmodel',
            name='build',
        ),
        migrations.RemoveField(
            model_name='roommodel',
            name='room',
        ),
    ]
