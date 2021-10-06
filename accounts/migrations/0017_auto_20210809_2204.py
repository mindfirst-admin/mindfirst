# Generated by Django 3.2.5 on 2021-08-09 21:04

import accounts.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0016_auto_20210727_2335'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='aspiration_name',
            field=models.CharField(default='Aspiration', max_length=255),
        ),
        migrations.AlterField(
            model_name='profile',
            name='user_token',
            field=models.CharField(default=accounts.models.generate_user_token, max_length=36),
        ),
    ]
