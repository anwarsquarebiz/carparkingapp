# Generated by Django 3.2.9 on 2023-07-07 21:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0002_parkingspot_reservation'),
    ]

    operations = [
        migrations.AddField(
            model_name='parkingspot',
            name='price_per_hour',
            field=models.DecimalField(decimal_places=2, default=50, max_digits=8),
        ),
    ]
