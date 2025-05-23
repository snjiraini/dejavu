"""
API Documentation helper module.
Contains decorators and utilities for documenting API endpoints using drf-yasg.
"""
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework import status
from .api_tags import AUTH_TAG, CATALOG_TAG, FINGERPRINTING_TAG, MONITORING_TAG

# Response schemas for common API responses
authentication_error_response = openapi.Response(
    description="Authentication error",
    examples={
        "application/json": {
            "detail": "Authentication credentials were not provided."
        }
    }
)

# Common parameters
track_id_param = openapi.Parameter(
    'track_id', 
    openapi.IN_PATH, 
    description="UUID of the track", 
    type=openapi.TYPE_STRING, 
    format=openapi.FORMAT_UUID
)

album_id_param = openapi.Parameter(
    'album_id', 
    openapi.IN_PATH, 
    description="UUID of the album", 
    type=openapi.TYPE_STRING, 
    format=openapi.FORMAT_UUID
)

artist_id_param = openapi.Parameter(
    'artist_id', 
    openapi.IN_PATH, 
    description="UUID of the artist", 
    type=openapi.TYPE_STRING, 
    format=openapi.FORMAT_UUID
)

audio_file_param = openapi.Parameter(
    'audio_file', 
    openapi.IN_FORM, 
    description="Audio file to analyze", 
    type=openapi.TYPE_FILE, 
    required=True
)

# Example responses
track_response_example = {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "title": "Song Title",
    "artist": {
        "id": "550e8400-e29b-41d4-a716-446655440001",
        "name": "Artist Name"
    },
    "album": {
        "id": "550e8400-e29b-41d4-a716-446655440002",
        "name": "Album Name"
    }
}

recognition_response_example = {
    "success": True,
    "results": [
        {
            "song_id": "550e8400-e29b-41d4-a716-446655440000",
            "song_name": "Song Title",
            "artist_name": "Artist Name",
            "confidence": 95.2,
            "offset_seconds": 2.5
        }
    ],
    "match_quality": {
        "processing_time": "1.25 seconds",
        "confidence_explanation": "Confidence shows what percentage of your audio matched the track"
    }
}

# Swagger documentation decorators
def track_list_docs(view_func):
    """Decorator for track_list view documentation"""
    return swagger_auto_schema(
        operation_description="Get a list of all tracks in the catalog",
        operation_summary="List all tracks",
        tags=[CATALOG_TAG],
        responses={
            status.HTTP_200_OK: openapi.Response(
                description="List of tracks",
                examples={"application/json": [track_response_example]}
            ),
            status.HTTP_401_UNAUTHORIZED: authentication_error_response
        }
    )(view_func)

def track_detail_docs(view_func):
    """Decorator for track_detail view documentation"""
    return swagger_auto_schema(
        operation_description="Get details of a specific track by ID",
        operation_summary="Get track details",
        tags=[CATALOG_TAG],
        manual_parameters=[track_id_param],
        responses={
            status.HTTP_200_OK: openapi.Response(
                description="Track details",
                examples={"application/json": track_response_example}
            ),
            status.HTTP_404_NOT_FOUND: openapi.Response(description="Track not found")
        }
    )(view_func)

def recognize_audio_docs(view_func):
    """Decorator for recognize_audio view documentation"""
    return swagger_auto_schema(
        operation_description="Recognize a song from an audio file",
        operation_summary="Recognize audio",
        tags=[FINGERPRINTING_TAG],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'audio_file': openapi.Schema(type=openapi.TYPE_FILE, description='Audio file to recognize')
            },
            required=['audio_file']
        ),
        responses={
            status.HTTP_200_OK: openapi.Response(
                description="Recognition results",
                examples={"application/json": recognition_response_example}
            )
        }
    )(view_func)

def login_docs(view_func):
    """Decorator for login view documentation"""
    return swagger_auto_schema(
        operation_description="Log in a user and obtain authentication tokens",
        operation_summary="User login",
        tags=[AUTH_TAG],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING, description='Username'),
                'password': openapi.Schema(type=openapi.TYPE_STRING, description='Password'),
            },
            required=['username', 'password']
        ),
        responses={
            status.HTTP_200_OK: openapi.Response(
                description="Login successful",
                examples={"application/json": {
                    "token": "jwt-token-value",
                    "user": {
                        "id": 1,
                        "username": "username",
                        "email": "user@example.com"
                    }
                }}
            ),
            status.HTTP_401_UNAUTHORIZED: openapi.Response(
                description="Invalid credentials",
                examples={"application/json": {"error": "Invalid credentials"}}
            )
        }
    )(view_func)

# More documentation decorators for other endpoints
def album_list_docs(view_func):
    """Decorator for album_list view documentation"""
    return swagger_auto_schema(
        operation_description="Get a list of all albums in the catalog",
        operation_summary="List all albums",
        tags=[CATALOG_TAG],
        responses={
            status.HTTP_200_OK: openapi.Response(
                description="List of albums",
                examples={"application/json": [{
                    "album_id": "550e8400-e29b-41d4-a716-446655440002",
                    "title": "Album Title",
                    "release_date": "2023-01-01"
                }]}
            ),
            status.HTTP_401_UNAUTHORIZED: authentication_error_response
        }
    )(view_func)

def artist_list_docs(view_func):
    """Decorator for artist_list view documentation"""
    return swagger_auto_schema(
        operation_description="Get a list of all artists in the catalog",
        operation_summary="List all artists",
        tags=[CATALOG_TAG],
        responses={
            status.HTTP_200_OK: openapi.Response(
                description="List of artists",
                examples={"application/json": [{
                    "artist_id": "550e8400-e29b-41d4-a716-446655440001",
                    "name": "Artist Name",
                    "bio": "Artist biography"
                }]}
            ),
            status.HTTP_401_UNAUTHORIZED: authentication_error_response
        }
    )(view_func)

def airplay_logs_docs(view_func):
    """Decorator for airplay_logs view documentation"""
    return swagger_auto_schema(
        operation_description="Get a list of all airplay logs",
        operation_summary="List all airplay logs",
        tags=[MONITORING_TAG],
        responses={
            status.HTTP_200_OK: openapi.Response(
                description="List of airplay logs",
                examples={"application/json": [{
                    "log_id": "550e8400-e29b-41d4-a716-446655440003",
                    "station": "Radio Station",
                    "track": "Track Title",
                    "timestamp": "2023-01-01T12:00:00Z"
                }]}
            ),
            status.HTTP_401_UNAUTHORIZED: authentication_error_response
        }
    )(view_func)

def fingerprint_song_docs(view_func):
    """Decorator for fingerprint_song view documentation"""
    return swagger_auto_schema(
        operation_description="Fingerprint an audio file and add it to the database",
        operation_summary="Fingerprint song",
        tags=[FINGERPRINTING_TAG],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'audio_file': openapi.Schema(type=openapi.TYPE_FILE, description='Audio file to fingerprint'),
                'title': openapi.Schema(type=openapi.TYPE_STRING, description='Song title'),
                'artist': openapi.Schema(type=openapi.TYPE_STRING, description='Artist name'),
                'album': openapi.Schema(type=openapi.TYPE_STRING, description='Album name', required=False)
            },
            required=['audio_file', 'title', 'artist']
        ),
        responses={
            status.HTTP_200_OK: openapi.Response(
                description="Fingerprinting successful",
                examples={"application/json": {
                    "success": True,
                    "track_id": "550e8400-e29b-41d4-a716-446655440000",
                    "fingerprints_added": 1000
                }}
            )
        }
    )(view_func)
