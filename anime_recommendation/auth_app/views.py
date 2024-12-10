from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from anime_api.models import User


@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    username = request.data.get('username')
    password = request.data.get('password')
    email = request.data.get('email')
    preferred_genres = request.data.get('preferred_genres', [])  # Expecting a list of genres
    watched_anime = request.data.get('watched_anime', [])  # Expecting a list of watched anime IDs

    # Validate that both `preferred_genres` and `watched_anime` are lists
    if not isinstance(preferred_genres, list):
        return Response({"error": "Preferred genres must be a list"}, status=status.HTTP_400_BAD_REQUEST)
    if not isinstance(watched_anime, list):
        return Response({"error": "Watched anime must be a list"}, status=status.HTTP_400_BAD_REQUEST)

    # Check if username already exists
    if User.objects.filter(username=username).exists():
        return Response({"error": "Username already exists"}, status=status.HTTP_400_BAD_REQUEST)

    # Create the user and save their preferences
    user = User.objects.create_user(username=username, password=password, email=email)
    user.preferred_genres = ",".join(preferred_genres)  # Save preferred genres as CSV string
    user.watched_anime = ",".join(map(str, watched_anime))  # Save watched anime as CSV string
    user.save()

    return Response(
        {
            "message": "User created successfully",
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "preferred_genres": preferred_genres,
                "watched_anime": watched_anime,
            },
        },
        status=status.HTTP_201_CREATED,
    )


@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(username=username, password=password)

    if user is not None:
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }, status=status.HTTP_200_OK)
    return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)
