# Generated by Django 3.1.6 on 2021-07-20 19:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('package_name', models.CharField(max_length=20)),
                ('price', models.IntegerField(default=0)),
                ('subscription_date', models.DateField(auto_now_add=True)),
                ('last_amount_paid', models.IntegerField()),
                ('next_amount_to_be_paid', models.IntegerField()),
                ('customer_id', models.CharField(max_length=200)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
