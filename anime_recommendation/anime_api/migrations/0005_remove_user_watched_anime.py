# Generated by Django 5.1.4 on 2024-12-09 06:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('anime_api', '0004_animecache_average_score_animecache_description_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='watched_anime',
        ),
    ]
