import requests
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import redirect, render

@api_view(['GET'])
def search_anime(request):
    character_name = request.query_params.get('name', '').strip()  # Get the name parameter
    genre = request.query_params.get('genre', '').split()  # Get the genre parameter
    genre = [g.strip() for g in genre]

    if not character_name and not genre:
        return Response({"error": "Please provide at least one query parameter: 'name' or 'genre'"}, status=400)

    url = "https://graphql.anilist.co"
    
    # Construct the GraphQL query dynamically based on the parameters

    query = """
    query ($search: String, $genre: [String]) {
        Page {
            media(search: $search, genre_in: $genre, type: ANIME) {
                id
                title {
                    romaji
                    english
                    native
                }
                description
                episodes
                genres
                averageScore
            }
        }
    }
    """
    
    variables = {}
    if character_name:
        variables["search"] = character_name
    if genre:
        variables["genre"] = genre

    try:
        response = requests.post(url, json={'query': query, 'variables': variables})
        response.raise_for_status()  # Raise an error for HTTP issues
        data = response.json()

        if 'errors' in data:
            return Response({"error": data['errors']}, status=400)

        # Extract anime list from the response
        anime_list = data.get('data', {}).get('Page', {}).get('media', [])

        if anime_list:
            return Response(anime_list)

        return Response({"error": "No anime found matching the given criteria"}, status=404)

    except requests.exceptions.RequestException as e:
        return Response({"error": "Failed to connect to AniList API", "details": str(e)}, status=500)


@api_view(['GET'])
def recommendations(request):
    user = request.user  # Assuming the user is authenticated

    # Retrieve user preferences from the database
    preferred_genres = user.preferred_genres.split(",") if user.preferred_genres else []
    watched_anime = user.watched_anime.split(",") if user.watched_anime else []

    # If both preferred_genres and watched_anime are empty, return an error
    if not preferred_genres and not watched_anime:
        return Response({"error": "No preferred genres or watched anime found for the user"}, status=400)

    url = "https://graphql.anilist.co"
    
    # GraphQL query with variables
    query = """
    query ($genres: [String]) {
      Page {
        media(genre_in: $genres, type: ANIME) {
          id
          title {
            romaji
            english
            native
          }
          genres
          averageScore
        }
      }
    }
    """
    
    # Define variables for genres
    variables = {}
    if preferred_genres:
        variables["genres"] = preferred_genres
    if watched_anime:
        variables["watchedAnime"] = list(map(int, watched_anime))  # Convert to integers

    print("GraphQL Query:", query)  # Print the query
    print("Variables:", variables)  # Print the variables to check the format

    try:
        response = requests.post(url, json={'query': query, 'variables': variables})
        response.raise_for_status()  # Raise an error for HTTP issues
        print("Response:", response.text)  # Print the full response body
        data = response.json()

        # Check for GraphQL errors
        if 'errors' in data:
            return Response({"error": data['errors']}, status=400)

        # Extract anime list from the response
        anime_list = data.get('data', {}).get('Page', {}).get('media', [])

        if anime_list:
            return Response(anime_list)

        return Response({"message": "No anime recommendations found for the given criteria"}, status=404)

    except requests.exceptions.RequestException as e:
        return Response({"error": "Failed to connect to AniList API", "details": str(e)}, status=500)


# Home page view that redirects to the anime_recommendation page
def home(request):
    return render(request, 'anime_api/anime_recommendation.html')  # Redirect to anime_recommendation view