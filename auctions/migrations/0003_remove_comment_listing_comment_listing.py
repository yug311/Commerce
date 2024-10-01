# Generated by Django 5.0.1 on 2024-01-05 20:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_listing_comment_bid'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='listing',
        ),
        migrations.AddField(
            model_name='comment',
            name='listing',
            field=models.ManyToManyField(blank=True, related_name='comments', to='auctions.listing'),
        ),
    ]
