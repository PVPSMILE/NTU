# Generated by Django 4.1.5 on 2023-01-08 11:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('register', '0006_remove_registrationmodel_is_active_and_more'),
        ('news', '0016_chatmodel'),
    ]

    operations = [
        migrations.AddField(
            model_name='chatmodel',
            name='guest',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='guest', to='register.registrationmodel'),
        ),
    ]
