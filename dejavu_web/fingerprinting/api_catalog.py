from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
from .models import Track, Album, Artist, AudioFile, TrackArtist
from .decorators import role_required
import uuid

# CRUD for Tracks
@csrf_exempt
@role_required(['catalog_admin', 'superuser'])
def track_list(request):
    """List or create tracks"""
    if request.method == 'GET':
        tracks = Track.objects.all()
        data = [{
            'track_id': str(track.track_id),
            'title': track.title,
            'duration': track.duration,
            'isrc': track.isrc,
            'album': track.album.title if track.album else None,
        } for track in tracks]
        return JsonResponse({'tracks': data})
    
    elif request.method == 'POST':
        data = json.loads(request.body)
        album_id = data.get('album_id')
        album = None
        if album_id:
            try:
                album = Album.objects.get(album_id=album_id)
            except Album.DoesNotExist:
                return JsonResponse({'error': 'Album not found'}, status=404)
        
        track = Track.objects.create(
            title=data.get('title'),
            duration=data.get('duration'),
            isrc=data.get('isrc'),
            lyrics=data.get('lyrics'),
            album=album,
            file_hash=data.get('file_hash', str(uuid.uuid4())),  # Temporary hash if not provided
            total_hashes=data.get('total_hashes', 0)
        )
        
        # Link artists if provided
        artist_ids = data.get('artist_ids', [])
        for artist_id in artist_ids:
            try:
                artist = Artist.objects.get(artist_id=artist_id)
                TrackArtist.objects.create(track=track, artist=artist, role=data.get('role'))
            except Artist.DoesNotExist:
                pass
        
        return JsonResponse({
            'success': True,
            'track_id': str(track.track_id),
            'title': track.title
        }, status=201)

@csrf_exempt
@role_required(['catalog_admin', 'superuser'])
def track_detail(request, track_id):
    """Retrieve, update or delete a track"""
    try:
        track = Track.objects.get(track_id=track_id)
    except Track.DoesNotExist:
        return JsonResponse({'error': 'Track not found'}, status=404)
    
    if request.method == 'GET':
        # Detailed track info with artist and album details
        artists = [{
            'artist_id': str(ta.artist.artist_id),
            'name': ta.artist.name,
            'role': ta.role
        } for ta in track.trackartist_set.all()]
        
        audio_files = [{
            'id': str(af.audio_file_id),
            'format': af.format,
            'bitrate': af.bitrate,
            'path': af.storage_path
        } for af in track.audiofile_set.all()]
        
        data = {
            'track_id': str(track.track_id),
            'title': track.title,
            'duration': track.duration,
            'isrc': track.isrc,
            'lyrics': track.lyrics,
            'album': {
                'album_id': str(track.album.album_id),
                'title': track.album.title
            } if track.album else None,
            'artists': artists,
            'audio_files': audio_files,
            'file_hash': track.file_hash,
            'total_hashes': track.total_hashes,
            'created_at': track.created_at.isoformat(),
            'updated_at': track.updated_at.isoformat(),
        }
        return JsonResponse(data)
    
    elif request.method == 'PUT':
        data = json.loads(request.body)
        
        # Update album if provided
        if data.get('album_id'):
            try:
                track.album = Album.objects.get(album_id=data['album_id'])
            except Album.DoesNotExist:
                return JsonResponse({'error': 'Album not found'}, status=404)
        
        # Update track fields
        track.title = data.get('title', track.title)
        track.duration = data.get('duration', track.duration)
        track.isrc = data.get('isrc', track.isrc)
        track.lyrics = data.get('lyrics', track.lyrics)
        track.save()
        
        # Update artists if provided
        if 'artist_ids' in data:
            # Clear existing artists
            track.trackartist_set.all().delete()
            
            # Add new artists
            for artist_id in data['artist_ids']:
                try:
                    artist = Artist.objects.get(artist_id=artist_id)
                    TrackArtist.objects.create(track=track, artist=artist, role=data.get('role'))
                except Artist.DoesNotExist:
                    pass
        
        return JsonResponse({
            'success': True,
            'track_id': str(track.track_id),
            'title': track.title
        })
    
    elif request.method == 'DELETE':
        track.delete()
        return JsonResponse({'success': True})

# CRUD for Albums
@csrf_exempt
@role_required(['catalog_admin', 'superuser'])
def album_list(request):
    """List or create albums"""
    if request.method == 'GET':
        albums = Album.objects.all()
        data = [{
            'album_id': str(album.album_id),
            'title': album.title,
            'release_date': album.release_date.isoformat() if album.release_date else None,
            'created_at': album.created_at.isoformat(),
            'updated_at': album.updated_at.isoformat(),
        } for album in albums]
        return JsonResponse({'albums': data})
    
    elif request.method == 'POST':
        data = json.loads(request.body)
        
        album = Album.objects.create(
            title=data.get('title'),
            release_date=data.get('release_date')
        )
        
        return JsonResponse({
            'success': True,
            'album_id': str(album.album_id),
            'title': album.title
        }, status=201)

@csrf_exempt
@role_required(['catalog_admin', 'superuser'])
def album_detail(request, album_id):
    """Retrieve, update or delete an album"""
    try:
        album = Album.objects.get(album_id=album_id)
    except Album.DoesNotExist:
        return JsonResponse({'error': 'Album not found'}, status=404)
    
    if request.method == 'GET':
        # Get tracks in this album
        tracks = Track.objects.filter(album=album)
        track_data = [{
            'track_id': str(track.track_id),
            'title': track.title,
            'duration': track.duration,
        } for track in tracks]
        
        data = {
            'album_id': str(album.album_id),
            'title': album.title,
            'release_date': album.release_date.isoformat() if album.release_date else None,
            'created_at': album.created_at.isoformat(),
            'updated_at': album.updated_at.isoformat(),
            'tracks': track_data
        }
        return JsonResponse(data)
    
    elif request.method == 'PUT':
        data = json.loads(request.body)
        
        album.title = data.get('title', album.title)
        album.release_date = data.get('release_date', album.release_date)
        album.save()
        
        return JsonResponse({
            'success': True,
            'album_id': str(album.album_id),
            'title': album.title
        })
    
    elif request.method == 'DELETE':
        album.delete()
        return JsonResponse({'success': True})

# CRUD for Artists
@csrf_exempt
@role_required(['catalog_admin', 'superuser'])
def artist_list(request):
    """List or create artists"""
    if request.method == 'GET':
        artists = Artist.objects.all()
        data = [{
            'artist_id': str(artist.artist_id),
            'name': artist.name,
            'type': artist.type,
            'bio': artist.bio,
            'created_at': artist.created_at.isoformat(),
            'updated_at': artist.updated_at.isoformat(),
        } for artist in artists]
        return JsonResponse({'artists': data})
    
    elif request.method == 'POST':
        data = json.loads(request.body)
        
        artist = Artist.objects.create(
            name=data.get('name'),
            type=data.get('type', 'solo'),
            bio=data.get('bio', '')
        )
        
        return JsonResponse({
            'success': True,
            'artist_id': str(artist.artist_id),
            'name': artist.name
        }, status=201)

@csrf_exempt
@role_required(['catalog_admin', 'superuser'])
def artist_detail(request, artist_id):
    """Retrieve, update or delete an artist"""
    try:
        artist = Artist.objects.get(artist_id=artist_id)
    except Artist.DoesNotExist:
        return JsonResponse({'error': 'Artist not found'}, status=404)
    
    if request.method == 'GET':
        # Get tracks by this artist
        track_artists = TrackArtist.objects.filter(artist=artist).select_related('track')
        track_data = [{
            'track_id': str(ta.track.track_id),
            'title': ta.track.title,
            'role': ta.role
        } for ta in track_artists]
        
        data = {
            'artist_id': str(artist.artist_id),
            'name': artist.name,
            'type': artist.type,
            'bio': artist.bio,
            'created_at': artist.created_at.isoformat(),
            'updated_at': artist.updated_at.isoformat(),
            'tracks': track_data
        }
        return JsonResponse(data)
    
    elif request.method == 'PUT':
        data = json.loads(request.body)
        
        artist.name = data.get('name', artist.name)
        artist.type = data.get('type', artist.type)
        artist.bio = data.get('bio', artist.bio)
        artist.save()
        
        return JsonResponse({
            'success': True,
            'artist_id': str(artist.artist_id),
            'name': artist.name
        })
    
    elif request.method == 'DELETE':
        artist.delete()
        return JsonResponse({'success': True})

# CRUD for Audio Files
@csrf_exempt
@role_required(['catalog_admin', 'superuser'])
def audio_file_list(request):
    """List or create audio files"""
    if request.method == 'GET':
        audio_files = AudioFile.objects.all().select_related('track')
        data = [{
            'audio_file_id': str(af.audio_file_id),
            'track': {
                'track_id': str(af.track.track_id),
                'title': af.track.title
            },
            'format': af.format,
            'bitrate': af.bitrate,
            'storage_path': af.storage_path,
            'created_at': af.created_at.isoformat(),
            'updated_at': af.updated_at.isoformat(),
        } for af in audio_files]
        return JsonResponse({'audio_files': data})
    
    elif request.method == 'POST':
        data = json.loads(request.body)
        
        try:
            track = Track.objects.get(track_id=data.get('track_id'))
        except Track.DoesNotExist:
            return JsonResponse({'error': 'Track not found'}, status=404)
        
        audio_file = AudioFile.objects.create(
            track=track,
            format=data.get('format'),
            bitrate=data.get('bitrate'),
            storage_path=data.get('storage_path')
        )
        
        return JsonResponse({
            'success': True,
            'audio_file_id': str(audio_file.audio_file_id),
            'track_title': track.title
        }, status=201)

@csrf_exempt
@role_required(['catalog_admin', 'superuser'])
def audio_file_detail(request, audio_file_id):
    """Retrieve, update or delete an audio file"""
    try:
        audio_file = AudioFile.objects.get(audio_file_id=audio_file_id)
    except AudioFile.DoesNotExist:
        return JsonResponse({'error': 'Audio file not found'}, status=404)
    
    if request.method == 'GET':
        data = {
            'audio_file_id': str(audio_file.audio_file_id),
            'track': {
                'track_id': str(audio_file.track.track_id),
                'title': audio_file.track.title
            },
            'format': audio_file.format,
            'bitrate': audio_file.bitrate,
            'storage_path': audio_file.storage_path,
            'created_at': audio_file.created_at.isoformat(),
            'updated_at': audio_file.updated_at.isoformat(),
        }
        return JsonResponse(data)
    
    elif request.method == 'PUT':
        data = json.loads(request.body)
        
        if data.get('track_id'):
            try:
                audio_file.track = Track.objects.get(track_id=data['track_id'])
            except Track.DoesNotExist:
                return JsonResponse({'error': 'Track not found'}, status=404)
        
        audio_file.format = data.get('format', audio_file.format)
        audio_file.bitrate = data.get('bitrate', audio_file.bitrate)
        audio_file.storage_path = data.get('storage_path', audio_file.storage_path)
        audio_file.save()
        
        return JsonResponse({
            'success': True,
            'audio_file_id': str(audio_file.audio_file_id),
            'track_title': audio_file.track.title
        })
    
    elif request.method == 'DELETE':
        audio_file.delete()
        return JsonResponse({'success': True}) 