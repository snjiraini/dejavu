# Connecting the Frontend to the Django Backend

This document provides instructions on how to connect the React frontend to the Django backend.

## Overview

The frontend is a Next.js application that communicates with the Django backend using RESTful API calls.
Authentication is handled using JWT (JSON Web Tokens).

## API Endpoints

The Django backend exposes the following API endpoints:

### Authentication

- `POST /api/token/` - Get JWT token with username and password
- `POST /api/token/refresh/` - Refresh JWT token
- `GET /api/auth/me/` - Get current user info
- `POST /api/auth/login/` - Session-based login (alternative to JWT)
- `POST /api/auth/logout/` - Session-based logout
- `POST /api/auth/users/` - Create a new user (admin only)
- `GET /api/auth/users/list/` - List all users (admin only)

### Catalog Management

- `GET /api/catalog/tracks/` - List all tracks
- `POST /api/catalog/tracks/` - Create a new track
- `GET /api/catalog/tracks/<uuid>/` - Get track details
- `PUT /api/catalog/tracks/<uuid>/` - Update a track
- `DELETE /api/catalog/tracks/<uuid>/` - Delete a track

- `GET /api/catalog/albums/` - List all albums
- `POST /api/catalog/albums/` - Create a new album
- `GET /api/catalog/albums/<uuid>/` - Get album details
- `PUT /api/catalog/albums/<uuid>/` - Update an album
- `DELETE /api/catalog/albums/<uuid>/` - Delete an album

- `GET /api/catalog/artists/` - List all artists
- `POST /api/catalog/artists/` - Create a new artist
- `GET /api/catalog/artists/<uuid>/` - Get artist details
- `PUT /api/catalog/artists/<uuid>/` - Update an artist
- `DELETE /api/catalog/artists/<uuid>/` - Delete an artist

- `GET /api/catalog/audio-files/` - List all audio files
- `POST /api/catalog/audio-files/` - Create a new audio file
- `GET /api/catalog/audio-files/<uuid>/` - Get audio file details
- `PUT /api/catalog/audio-files/<uuid>/` - Update an audio file
- `DELETE /api/catalog/audio-files/<uuid>/` - Delete an audio file

### Radio Monitoring

- `GET /api/monitoring/airplay-logs/` - List airplay logs (with filters)
- `GET /api/monitoring/airplay-logs/<uuid>/` - Get airplay log details
- `POST /api/monitoring/airplay-logs/create/` - Create a new airplay log
- `DELETE /api/monitoring/airplay-logs/<uuid>/delete/` - Delete an airplay log

- `GET /api/monitoring/stations/` - List all radio stations
- `POST /api/monitoring/stations/` - Create a new radio station
- `GET /api/monitoring/stations/<uuid>/` - Get radio station details
- `PUT /api/monitoring/stations/<uuid>/` - Update a radio station
- `DELETE /api/monitoring/stations/<uuid>/` - Delete a radio station

## Running the Application

### 1. Start the Django Backend

```bash
cd dejavu_web
python manage.py runserver
```

The backend will be available at http://localhost:8000

### 2. Start the Frontend

```bash
cd dejavu_frontend
npm install
npm run dev
```

The frontend will be available at http://localhost:3000

## API Services

The frontend uses a set of API services to communicate with the backend:

- `authService.ts` - Handles authentication and user information
- `trackService.ts` - Manages track data
- `airplayService.ts` - Handles radio airplay logs

All API services use the `axiosClient.ts` file, which configures Axios with:

- Base URL configuration
- JWT authentication header
- Token refresh logic
- Error handling

## CORS Configuration

If you encounter CORS (Cross-Origin Resource Sharing) issues, make sure your Django backend has CORS properly configured.

To install Django CORS headers:

```bash
pip install django-cors-headers
```

Add to your Django settings:

```python
INSTALLED_APPS = [
    # ...
    'corsheaders',
    # ...
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # Add this before CommonMiddleware
    # ...
]

# During development
CORS_ALLOW_ALL_ORIGINS = True  # For development only
# Or for production
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "https://yourdomain.com",
]
```

## Troubleshooting

### Authentication Issues

- Make sure the JWT tokens are being stored properly in localStorage
- Check that the token is being included in the Authorization header
- Verify that the token is valid and not expired

### API Connection Issues

- Confirm the backend server is running
- Check that the base URL in `axiosClient.ts` is correct
- Look for CORS issues in the browser developer console
- Verify network requests/responses in the browser developer tools

### Data Not Loading

- Check for errors in the console
- Verify the API endpoint URLs
- Ensure the data formatting matches between frontend and backend
