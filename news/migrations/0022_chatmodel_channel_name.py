# Generated by Django 4.1.5 on 2023-01-09 20:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0021_remove_messagemodel_sender'),
    ]

    operations = [
        migrations.AddField(
            model_name='chatmodel',
            name='channel_name',
            field=models.CharField(max_length=300, null=True, verbose_name='Channel Name'),
        ),
    ]