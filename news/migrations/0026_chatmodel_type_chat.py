# Generated by Django 4.1.5 on 2023-01-12 13:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0025_typeofchat_friendmodel_owner'),
    ]

    operations = [
        migrations.AddField(
            model_name='chatmodel',
            name='type_chat',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='news.typeofchat'),
        ),
    ]