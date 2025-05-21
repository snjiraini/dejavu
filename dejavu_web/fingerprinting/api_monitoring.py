from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
from .models import RadioStation, RadioAirplayLog, Track, TrackArtist
from .decorators import role_required
from django.db.models import Count, Sum
from datetime import datetime, timedelta

@csrf_exempt
@role_required(['radio_monitor', 'business_analyst', 'rights_holder', 'artist', 'label', 'superuser'])
def airplay_logs(request):
    """Get radio airplay logs with filtering"""
    # Default to last 7 days
    start_date = request.GET.get('start_date', (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d'))
    end_date = request.GET.get('end_date', datetime.now().strftime('%Y-%m-%d'))
    
    # Convert to datetime objects
    start_date = datetime.strptime(start_date, '%Y-%m-%d')
    end_date = datetime.strptime(end_date, '%Y-%m-%d') + timedelta(days=1)  # Include end date
    
    # Base queryset
    queryset = RadioAirplayLog.objects.filter(
        played_at__gte=start_date,
        played_at__lt=end_date
    )
    
    # Filter by station if provided
    station_id = request.GET.get('station_id')
    if station_id:
        queryset = queryset.filter(station_id=station_id)
    
    # Filter by track if provided
    track_id = request.GET.get('track_id')
    if track_id:
        queryset = queryset.filter(track_id=track_id)
    
    # For artists/labels, only show their tracks
    if request.user.has_role('artist') or request.user.has_role('label'):
        if hasattr(request.user, 'associated_artist') and request.user.associated_artist:
            artist_id = request.user.associated_artist.artist_id
            # Get tracks by this artist
            track_ids = TrackArtist.objects.filter(artist_id=artist_id).values_list('track_id', flat=True)
            queryset = queryset.filter(track_id__in=track_ids)
    
    # Paginate results
    page = int(request.GET.get('page', 1))
    page_size = int(request.GET.get('page_size', 50))
    start = (page - 1) * page_size
    end = start + page_size
    
    # Get data with related objects
    queryset = queryset.select_related('track', 'station')
    
    logs = [{
        'log_id': str(log.log_id),
        'track': {
            'track_id': str(log.track.track_id),
            'title': log.track.title,
        },
        'station': {
            'station_id': str(log.station.station_id),
            'name': log.station.name,
            'location': log.station.location
        },
        'played_at': log.played_at.isoformat(),
        'confidence_score': float(log.confidence_score) if log.confidence_score else None
    } for log in queryset[start:end]]
    
    return JsonResponse({
        'logs': logs,
        'total': queryset.count(),
        'page': page,
        'page_size': page_size
    })

@csrf_exempt
@role_required(['radio_monitor', 'superuser'])
def create_airplay_log(request):
    """Manual creation of airplay logs (for radio monitors)"""
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    data = json.loads(request.body)
    
    try:
        track = Track.objects.get(track_id=data.get('track_id'))
        station = RadioStation.objects.get(station_id=data.get('station_id'))
    except (Track.DoesNotExist, RadioStation.DoesNotExist):
        return JsonResponse({'error': 'Track or station not found'}, status=404)
    
    # Create the log
    try:
        played_at = datetime.strptime(data.get('played_at'), '%Y-%m-%d %H:%M:%S')
    except (ValueError, TypeError):
        return JsonResponse({'error': 'Invalid date format for played_at. Use YYYY-MM-DD HH:MM:SS'}, status=400)
    
    log = RadioAirplayLog.objects.create(
        track=track,
        station=station,
        played_at=played_at,
        confidence_score=data.get('confidence_score')
    )
    
    return JsonResponse({
        'success': True,
        'log_id': str(log.log_id)
    }, status=201)

@csrf_exempt
@role_required(['radio_monitor', 'superuser'])
def delete_airplay_log(request, log_id):
    """Delete an airplay log"""
    try:
        log = RadioAirplayLog.objects.get(log_id=log_id)
    except RadioAirplayLog.DoesNotExist:
        return JsonResponse({'error': 'Log not found'}, status=404)
    
    log.delete()
    return JsonResponse({'success': True})

@csrf_exempt
@role_required(['radio_monitor', 'superuser'])
def airplay_log_detail(request, log_id):
    """Get detail of a specific airplay log"""
    try:
        log = RadioAirplayLog.objects.get(log_id=log_id)
    except RadioAirplayLog.DoesNotExist:
        return JsonResponse({'error': 'Log not found'}, status=404)
    
    data = {
        'log_id': str(log.log_id),
        'track': {
            'track_id': str(log.track.track_id),
            'title': log.track.title,
        },
        'station': {
            'station_id': str(log.station.station_id),
            'name': log.station.name,
            'location': log.station.location
        },
        'played_at': log.played_at.isoformat(),
        'confidence_score': float(log.confidence_score) if log.confidence_score else None,
        'created_at': log.created_at.isoformat()
    }
    
    return JsonResponse(data)

# CRUD for Radio Stations
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
            'created_at': station.created_at.isoformat(),
            'updated_at': station.updated_at.isoformat(),
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
            'station_id': str(station.station_id),
            'name': station.name
        }, status=201)

@csrf_exempt
@role_required(['radio_monitor', 'superuser'])
def station_detail(request, station_id):
    """Retrieve, update or delete a radio station"""
    try:
        station = RadioStation.objects.get(station_id=station_id)
    except RadioStation.DoesNotExist:
        return JsonResponse({'error': 'Station not found'}, status=404)
    
    if request.method == 'GET':
        # Get recent airplays at this station
        logs = RadioAirplayLog.objects.filter(
            station=station
        ).order_by('-played_at')[:20].select_related('track')
        
        log_data = [{
            'log_id': str(log.log_id),
            'track': {
                'track_id': str(log.track.track_id),
                'title': log.track.title,
            },
            'played_at': log.played_at.isoformat(),
            'confidence_score': float(log.confidence_score) if log.confidence_score else None
        } for log in logs]
        
        data = {
            'station_id': str(station.station_id),
            'name': station.name,
            'location': station.location,
            'created_at': station.created_at.isoformat(),
            'updated_at': station.updated_at.isoformat(),
            'recent_airplays': log_data
        }
        return JsonResponse(data)
    
    elif request.method == 'PUT':
        data = json.loads(request.body)
        
        station.name = data.get('name', station.name)
        station.location = data.get('location', station.location)
        station.save()
        
        return JsonResponse({
            'success': True,
            'station_id': str(station.station_id),
            'name': station.name
        })
    
    elif request.method == 'DELETE':
        station.delete()
        return JsonResponse({'success': True}) 