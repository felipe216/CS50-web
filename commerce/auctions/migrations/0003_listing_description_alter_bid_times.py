# Generated by Django 4.2.5 on 2023-10-01 22:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_listing_bid'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='description',
            field=models.CharField(default='No category Listed', max_length=64),
        ),
        migrations.AlterField(
            model_name='bid',
            name='times',
            field=models.IntegerField(),
        ),
    ]
