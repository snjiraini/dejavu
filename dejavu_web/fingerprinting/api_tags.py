"""
API tags for organizing endpoints in Swagger documentation
"""

# Tag definitions
AUTH_TAG = "Authentication"
CATALOG_TAG = "Music Catalog"
FINGERPRINTING_TAG = "Fingerprinting & Recognition"
MONITORING_TAG = "Monitoring"

# Tag descriptions
TAG_DESCRIPTIONS = [
    {
        'name': AUTH_TAG,
        'description': 'Endpoints for user authentication, login, logout, and user management'
    },
    {
        'name': CATALOG_TAG,
        'description': 'Endpoints for managing music catalog: tracks, albums, and artists'
    },
    {
        'name': FINGERPRINTING_TAG,
        'description': 'Core endpoints for fingerprinting audio files and recognizing audio samples'
    },
    {
        'name': MONITORING_TAG,
        'description': 'Endpoints for monitoring radio airplay and track plays'
    }
]
