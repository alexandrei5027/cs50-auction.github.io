# Generated by Django 5.1.7 on 2025-03-29 15:14

import datetime
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0004_listing_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='expire',
            field=models.DateTimeField(default=datetime.datetime(2025, 3, 30, 15, 14, 46, 275999, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='listing',
            name='title',
            field=models.CharField(default='', max_length=50, validators=[django.core.validators.MinLengthValidator(5)]),
        ),
    ]
