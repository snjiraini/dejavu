from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import os
import json
from dejavu import Dejavu
from dejavu.logic.recognizer.file_recognizer import FileRecognizer
from .models import Track, Fingerprint, Artist, Album, AudioFile
from dejavu.config.settings import (
    DEFAULT_FAN_VALUE,
    PEAK_NEIGHBORHOOD_SIZE,
    DEFAULT_AMP_MIN,
    PEAK_SORT,
    CONNECTIVITY_MASK
)
from .api_docs import recognize_audio_docs, fingerprint_song_docs

def index(request):
    return render(request, 'fingerprinting/index.html')

def clean_for_json(obj):
    """Convert problematic types to JSON-serializable types."""
    if isinstance(obj, bytes):
        return obj.decode('utf-8', errors='replace')
    elif isinstance(obj, dict):
        return {k: clean_for_json(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [clean_for_json(item) for item in obj]
    elif hasattr(obj, 'dtype') and hasattr(obj, 'item'):  # Handle NumPy types
        return obj.item()
    elif str(type(obj)).startswith("<class 'numpy."):  # Fallback for NumPy types
        return int(obj) if hasattr(obj, '__int__') else float(obj) if hasattr(obj, '__float__') else str(obj)
    return obj
    return obj

@csrf_exempt
@recognize_audio_docs
def recognize_audio(request):
    if request.method == 'POST' and request.FILES.get('audio_file'):
        audio_file = request.FILES['audio_file']
        
        # Save the uploaded file temporarily
        temp_path = f"/tmp/{audio_file.name}"
        with open(temp_path, 'wb+') as destination:
            for chunk in audio_file.chunks():
                destination.write(chunk)
        
        print(f"Debug: Recognition - File saved to {temp_path}")
        
        # Initialize DejaVu with Django ORM using global settings
        config = {
            "database_type": "django",
            "models": {
                "Track": Track,  # Use Track model directly
                "Fingerprint": Fingerprint
            },
            "fingerprint_limit": None,  # Process the entire file
            "peak_neighborhood_size": PEAK_NEIGHBORHOOD_SIZE,
            "fan_value": DEFAULT_FAN_VALUE,
            "amp_min": DEFAULT_AMP_MIN,
            "peak_sort": PEAK_SORT,
            "connectivity_mask": CONNECTIVITY_MASK
        }
        
        print(f"Debug: Recognition - Initializing Dejavu")
        djv = Dejavu(config)
        
        # Check DB state before recognition
        tracks = list(Track.objects.all())
        print(f"Debug: Recognition - Found {len(tracks)} tracks in database")
        for track in tracks:
            fp_count = Fingerprint.objects.filter(track=track).count()
            print(f"Debug: Recognition - Track {track.title} has {fp_count} fingerprints")
        
        try:
            # Recognize the song
            print(f"Debug: Recognition - Starting recognition process")
            results = djv.recognize(FileRecognizer, temp_path)
            print(f"Debug: Recognition - Results: {results}")
            
            # Add some additional context if a match was found
            if results and 'results' in results and results['results']:
                # Add confidence information to help the user understand the match quality
                total_time = results.get('total_time', 0)
                
                # Calculate confidence percentage for each match
                for match in results['results']:
                    # Calculate input confidence percentage
                    input_hashes = match.get('input_total_hashes', 0)
                    hashes_matched = match.get('hashes_matched_in_input', 0)
                    confidence = (hashes_matched / input_hashes * 100) if input_hashes > 0 else 0
                    
                    # Add confidence percentage to the match
                    match['confidence'] = round(confidence, 2)
                
                results['match_quality'] = {
                    'processing_time': f"{total_time:.2f} seconds",
                    'confidence_explanation': "Confidence shows what percentage of your audio matched the track"
                }
            
            # Convert problematic types to JSON-serializable types
            results = clean_for_json(results)
            return JsonResponse(results)
        except Exception as e:
            import traceback
            traceback.print_exc()
            return JsonResponse({'error': str(e)}, status=500)
        finally:
            # Clean up
            if os.path.exists(temp_path):
                os.remove(temp_path)
    
    return JsonResponse({'error': 'Invalid request'}, status=400)

@csrf_exempt
def fingerprint_song(request):
    if request.method == 'POST' and request.FILES.get('audio_file'):
        audio_file = request.FILES['audio_file']
        track_title = request.POST.get('track_title', audio_file.name)  # Use track_title instead of song_name
        
        # Save the uploaded file temporarily
        temp_path = f"/tmp/{audio_file.name}"
        with open(temp_path, 'wb+') as destination:
            for chunk in audio_file.chunks():
                destination.write(chunk)
        
        # Initialize DejaVu with Django ORM using global settings
        config = {
            "database_type": "django",
            "models": {
                "Track": Track,  # Use Track model directly
                "Fingerprint": Fingerprint
            },
            "fingerprint_limit": None,  # Process the entire file
            "peak_neighborhood_size": PEAK_NEIGHBORHOOD_SIZE,
            "fan_value": DEFAULT_FAN_VALUE,
            "amp_min": DEFAULT_AMP_MIN,
            "peak_sort": PEAK_SORT,
            "connectivity_mask": CONNECTIVITY_MASK
        }
        
        djv = Dejavu(config)
        
        try:
            # Process the fingerprinting directly
            # Now using track_title since we've updated Dejavu to use it
            track_title, hashes, file_hash = Dejavu._fingerprint_worker(
                (temp_path, None), 
                track_title=track_title
            )
            
            # Check if track already exists
            existing_track = None
            try:
                existing_track = Track.objects.get(file_hash=file_hash)
                track_id = existing_track.track_id
                
                # Clear existing fingerprints for this track
                Fingerprint.objects.filter(track_id=track_id).delete()
            except Track.DoesNotExist:
                # Create new track directly (instead of using insert_song)
                new_track = Track.objects.create(
                    title=track_title,
                    file_hash=file_hash,
                    total_hashes=len(hashes)
                )
                track_id = new_track.track_id
                
                # Create default audio file for the track
                AudioFile.objects.create(
                    track=new_track,
                    format=temp_path.split('.')[-1] if '.' in temp_path else 'unknown',
                    storage_path=temp_path
                )
                
                # Get or create default artist
                default_artist, _ = Artist.objects.get_or_create(
                    name='Unknown Artist',
                    type='solo'
                )
                
                # Get or create default album
                default_album, _ = Album.objects.get_or_create(
                    title='Unknown Album'
                )
                
                # Link track to album
                new_track.album = default_album
                new_track.save()
            
            # Insert fingerprints directly for this track
            fingerprint_objects = []
            for hash_value, offset in hashes:
                fingerprint_objects.append(Fingerprint(
                    track_id=track_id,
                    hash=hash_value,
                    offset=offset
                ))
            
            # Use bulk_create for efficiency
            Fingerprint.objects.bulk_create(fingerprint_objects, batch_size=1000)
            
            # Verify fingerprints were saved
            fingerprint_count = Fingerprint.objects.filter(track_id=track_id).count()
            response_data = {
                'message': f'Successfully fingerprinted {track_title}',
                'hash_count': len(hashes),
                'fingerprints_stored': fingerprint_count
            }
            response_data = clean_for_json(response_data)
            return JsonResponse(response_data)
        except Exception as e:
            import traceback
            traceback.print_exc()
            return JsonResponse({'error': str(e)}, status=500)
        finally:
            # Clean up
            if os.path.exists(temp_path):
                os.remove(temp_path)
    
    return JsonResponse({'error': 'Invalid request'}, status=400)
