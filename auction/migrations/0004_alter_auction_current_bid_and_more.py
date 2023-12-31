# Generated by Django 4.2.2 on 2023-06-15 18:07

import auction.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auction', '0003_alter_auction_deadline_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auction',
            name='current_bid',
            field=models.BigIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='auction',
            name='deadline_date',
            field=models.DateField(blank=True, default=auction.models.Auction.seven_day_hence),
        ),
        migrations.AlterField(
            model_name='auction',
            name='is_auction_open',
            field=models.BooleanField(blank=True, default=True),
        ),
    ]
