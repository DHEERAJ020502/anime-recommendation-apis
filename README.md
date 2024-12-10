1. User Registration
Endpoint: /auth/register/
Method: POST
Request Body:
json
{
    "username": "string",
    "password": "string",
    "email": "string",
    "preferred_genres": ["genre1", "genre2"],
    "watched_anime": ["anime_id1", "anime_id2"]
}
Response: User details or error message.

2. User Login
Endpoint: /auth/login/
Method: POST
Description: Authenticates a user and provides JWT tokens.
Request Body:
json
{
    "username": "string",
    "password": "string"
}
Response: Access and refresh tokens or error message.

3. Search Anime
Endpoint: /anime/search/
Method: GET
Description: Searches for anime based on name and genres.
Query Parameters:
name: Partial or full name of the anime (optional).
genre: Comma-separated genres (optional).
Response: List of anime matching the criteria or an error message.

4. Get Recommendations
Endpoint: /anime/recommendations/
Method: GET
Description: Provides anime recommendations based on the authenticated user's preferences.
Response: List of recommended anime or an error message.
