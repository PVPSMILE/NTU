# Generated by Django 4.1.5 on 2023-01-06 15:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('register', '0006_remove_registrationmodel_is_active_and_more'),
        ('news', '0011_chatmodel_chanel_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='chatmodel',
            name='getter',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='getter', to='register.registrationmodel'),
        ),
    ]
