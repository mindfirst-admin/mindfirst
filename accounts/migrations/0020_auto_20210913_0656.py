# Generated by Django 3.2.5 on 2021-09-13 05:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0019_alter_profile_behaviors_done_this_week'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='behaviors_done_this_week',
            new_name='bad_behaviors_done_this_week',
        ),
        migrations.AddField(
            model_name='profile',
            name='good_behaviors_done_this_week',
            field=models.CharField(default='0/0', max_length=10),
        ),
    ]
