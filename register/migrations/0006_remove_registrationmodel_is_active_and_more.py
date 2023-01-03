# Generated by Django 4.1.4 on 2022-12-30 08:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0006_auto_20221228_1718'),
        ('register', '0005_registrationmodel_photo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='registrationmodel',
            name='is_active',
        ),
        migrations.AddField(
            model_name='registrationmodel',
            name='status',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='news.status'),
        ),
        migrations.AddField(
            model_name='registrationmodel',
            name='type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='news.typeofrequest'),
        ),
    ]