from django.db import models
from django.contrib.auth.models import AbstractUser

# Extend User model to include user preferences for recommendations
class User(AbstractUser):
    preferred_genres = models.TextField(blank=True) # User's favorite genres
    watched_anime = models.TextField(blank=True)  # List of watched anime

    # Set unique related names to avoid clashes with the default User model
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='anime_user_set',  # Avoids clash with default 'user_set'
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )
    
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='anime_user_permissions_set',  # Avoids clash with default 'user_permissions'
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

# AnimeCache model to store anime data fetched from AniList API
class AnimeCache(models.Model):
    anime_id = models.IntegerField(unique=True)  # Unique anime identifier from AniList
    name = models.CharField(max_length=255)  # Name of the anime
    genres = models.JSONField()  # List of genres for the anime
    popularity = models.IntegerField()  # Popularity score of the anime
    average_score = models.FloatField(default=0)  # Average score for the anime
    description = models.TextField(default="No description available")  # Brief description of the anime
    created_at = models.DateTimeField(auto_now_add=True)  # Date when this record was created

    def __str__(self):
        return self.name
