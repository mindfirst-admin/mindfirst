# Generated by Django 3.2.5 on 2021-09-04 05:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0017_auto_20210809_2204'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='behaviors_done_this_week',
            field=models.IntegerField(default=0),
        ),
    ]
