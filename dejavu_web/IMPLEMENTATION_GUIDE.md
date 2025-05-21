# Dejavu API Implementation Guide

This document outlines the step-by-step process for implementing the complete Dejavu API with role-based access control.

## Implementation Structure

The implementation follows a modular approach with these components:

1. **Models**: Custom User model with Role-based access control
2. **API Modules**: Separated by functional area
   - Authentication (`api_auth.py`)
   - Catalog Management (`api_catalog.py`)
   - Radio Monitoring (`api_monitoring.py`)
   - Reports & Analytics (`api_reports.py`)
3. **Decorators**: Role-based access control decorator (`decorators.py`)
4. **Management Commands**: For initial setup and data migration

## Completed Implementation

The following components have been implemented:

1. **Models**:

   - Custom User model with role-based access
   - Role model with predefined roles
   - Updated existing models with proper relationships

2. **API Decorators**:

   - `@role_required` decorator for access control

3. **Authentication API**:

   - Login/logout functionality
   - User creation (superuser only)
   - User listing (superuser only)

4. **Catalog Management API (Track endpoints)**:

   - List/Create tracks
   - View/Update/Delete individual tracks

5. **Management Commands**:
   - Create roles and superuser

## Next Steps for Full Implementation

To complete the implementation, follow these steps:

### 1. Complete Catalog Management API

Create the following endpoints in `api_catalog.py`:

- Album CRUD operations
- Artist CRUD operations
- AudioFile CRUD operations

Add these endpoints to `urls.py`.

### 2. Implement Radio Monitoring API

Create a new file `api_monitoring.py` with:

- Radio station CRUD operations
- Radio airplay log CRUD operations

Example implementation:

```python
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import RadioStation, RadioAirplayLog, Track
from .decorators import role_required
from datetime import datetime

@csrf_exempt
@role_required(['radio_monitor', 'superuser'])
def station_list(request):
    """List or create radio stations"""
    if request.method == 'GET':
        stations = RadioStation.objects.all()
        data = [{
            'station_id': str(station.station_id),
            'name': station.name,
            'location': station.location,
        } for station in stations]
        return JsonResponse({'stations': data})

    elif request.method == 'POST':
        data = json.loads(request.body)
        station = RadioStation.objects.create(
            name=data.get('name'),
            location=data.get('location')
        )
        return JsonResponse({
            'success': True,
            'station_id': str(station.station_id)
        }, status=201)

# Additional endpoints for station_detail, airplay_logs, create_airplay_log
```

### 3. Implement Reports & Analytics API

Create a new file `api_reports.py` with:

- Artist airplay report
- Track performance report
- Station analysis report
- Regional breakdown report

Example implementation:

```python
from django.http import JsonResponse
from .models import Track, Artist, RadioAirplayLog, TrackArtist
from .decorators import role_required
from django.db.models import Count
from datetime import datetime, timedelta

@role_required(['business_analyst', 'rights_holder', 'superuser'])
def artist_airplay_report(request):
    """Report on artist airplay statistics"""
    start_date = request.GET.get('start_date', (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d'))
    end_date = request.GET.get('end_date', datetime.now().strftime('%Y-%m-%d'))

    # Convert to datetime objects
    start_date = datetime.strptime(start_date, '%Y-%m-%d')
    end_date = datetime.strptime(end_date, '%Y-%m-%d') + timedelta(days=1)

    # Get artist data with play counts
    # (implementation details)

    return JsonResponse({'artists': result})

# Additional report endpoints
```

### 4. Update URLs Configuration

Update `urls.py` to include all endpoints:

```python
from django.urls import path
from . import views
from . import api_auth, api_catalog, api_monitoring, api_reports

urlpatterns = [
    # Existing endpoints

    # Add monitoring endpoints
    path('api/monitoring/stations/', api_monitoring.station_list, name='station_list'),
    path('api/monitoring/stations/<uuid:station_id>/', api_monitoring.station_detail, name='station_detail'),
    # ... more endpoints

    # Add reports endpoints
    path('api/reports/artist-airplay/', api_reports.artist_airplay_report, name='artist_airplay_report'),
    # ... more endpoints
]
```

### 5. Database Migration

Run migrations and the setup command:

```bash
python manage.py migrate
python manage.py create_roles_and_users
```

## Testing the API

Use tools like curl, Postman, or a Python script to test each endpoint:

1. **Login as superuser**:

   ```bash
   curl -X POST -H "Content-Type: application/json" -d '{"username":"admin","password":"adminpassword"}' http://localhost:8000/api/auth/login/
   ```

2. **Create a new track**:
   ```bash
   curl -X POST -H "Content-Type: application/json" -d '{"title":"Test Track","duration":180}' http://localhost:8000/api/catalog/tracks/
   ```

## Role-Based Access Rules

The following roles have specific access rights:

1. **Catalog Administrator**:

   - Full CRUD access to tracks, albums, artists, audio files

2. **Rights Holder**:

   - Read access to catalog
   - Access to reports

3. **Radio Monitor**:

   - Full CRUD access to radio stations and airplay logs
   - Read access to tracks

4. **Business Analyst**:

   - Read access to all reports

5. **Artist/Label**:

   - Read access to own tracks and airplay data

6. **Superuser**:
   - All access

## Conclusion

This implementation provides a comprehensive API with role-based access control for the Dejavu music fingerprinting system. By following the steps above, you can complete the full implementation and have a working system for managing tracks, monitoring radio plays, and generating reports based on user roles.
