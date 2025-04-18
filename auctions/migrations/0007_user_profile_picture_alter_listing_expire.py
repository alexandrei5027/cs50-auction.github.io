# Generated by Django 5.1.7 on 2025-04-01 15:00

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0006_alter_listing_expire_wishlist'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='profile_picture',
            field=models.ImageField(default=0, upload_to='profile_picture'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='listing',
            name='expire',
            field=models.DateTimeField(default=datetime.datetime(2025, 4, 2, 15, 0, 32, 109111, tzinfo=datetime.timezone.utc)),
        ),
    ]
