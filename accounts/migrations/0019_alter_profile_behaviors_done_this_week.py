# Generated by Django 3.2.5 on 2021-09-07 21:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0018_profile_behaviors_done_this_week'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='behaviors_done_this_week',
            field=models.CharField(default='0/0', max_length=10),
        ),
    ]
