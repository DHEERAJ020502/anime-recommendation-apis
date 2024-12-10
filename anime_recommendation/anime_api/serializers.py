from rest_framework import serializers
from .models import User, AnimeCache

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'preferred_genres']

class AnimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnimeCache
        fields = ['anime_id', 'name', 'genres', 'popularity']
