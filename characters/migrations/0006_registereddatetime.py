# Generated by Django 3.2.5 on 2021-09-02 19:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('characters', '0005_habitdesign_number_of_times'),
    ]

    operations = [
        migrations.CreateModel(
            name='RegisteredDateTime',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('current_time', models.TimeField(auto_now_add=True)),
                ('daily', models.BooleanField(default=False)),
                ('behavior', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='characters.behaviourmaps')),
            ],
        ),
    ]
