# Generated by Django 3.2.5 on 2021-10-15 23:09

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserPurchases',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('purchase', models.CharField(default='', max_length=255)),
                ('stripe_customer_id', models.CharField(default='', max_length=255)),
                ('stripe_checkout_id', models.CharField(default='', max_length=255)),
                ('email', models.EmailField(default='', max_length=255)),
                ('date_paid', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
