# Generated by Django 5.1.7 on 2025-03-26 13:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_alter_listing_currentprice'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bid',
            old_name='user',
            new_name='user_id',
        ),
    ]
