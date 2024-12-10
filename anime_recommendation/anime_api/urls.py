from django.urls import path
from .views import search_anime, recommendations, home

urlpatterns = [
    path('', home, name='home'),
    path('anime/search/', search_anime,name = 'search_anime()'),
    path('anime/recommendations/', recommendations,name = 'recommendations()'),
]
