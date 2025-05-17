from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import os
import json
from dejavu import Dejavu
from dejavu.logic.recognizer.file_recognizer import FileRecognizer
from dejavu.logic.recognizer.microphone_recognizer import MicrophoneRecognizer
from .models import Song, Fingerprint

def index(request):
    return render(request, 'fingerprinting/index.html')

@csrf_exempt
def recognize_audio(request):
    if request.method == 'POST' and request.FILES.get('audio_file'):
        audio_file = request.FILES['audio_file']
        
        # Save the uploaded file temporarily
        temp_path = f"/tmp/{audio_file.name}"
        with open(temp_path, 'wb+') as destination:
            for chunk in audio_file.chunks():
                destination.write(chunk)
        
        print(f"Debug: Recognition - File saved to {temp_path}")
        
        # Initialize DejaVu with Django ORM
        config = {
            "database_type": "django",
            "models": {
                "Song": Song,
                "Fingerprint": Fingerprint
            }
        }
        
        print(f"Debug: Recognition - Initializing Dejavu")
        djv = Dejavu(config)
        
        # Check DB state before recognition
        songs = list(Song.objects.all())
        print(f"Debug: Recognition - Found {len(songs)} songs in database")
        for song in songs:
            fp_count = Fingerprint.objects.filter(song=song).count()
            print(f"Debug: Recognition - Song {song.song_name} has {fp_count} fingerprints")
        
        try:
            # Recognize the song
            print(f"Debug: Recognition - Starting recognition process")
            results = djv.recognize(FileRecognizer, temp_path)
            print(f"Debug: Recognition - Results: {results}")
            
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
        song_name = request.POST.get('song_name', audio_file.name)
        
        # Save the uploaded file temporarily
        temp_path = f"/tmp/{audio_file.name}"
        with open(temp_path, 'wb+') as destination:
            for chunk in audio_file.chunks():
                destination.write(chunk)
        
        # Initialize DejaVu with Django ORM
        config = {
            "database_type": "django",
            "models": {
                "Song": Song,
                "Fingerprint": Fingerprint
            }
        }
        
        djv = Dejavu(config)
        
        try:
            # Process the fingerprinting directly
            song_name, hashes, file_hash = Dejavu._fingerprint_worker(
                (temp_path, None), 
                song_name=song_name
            )
            
            # Check if song already exists
            existing_song = None
            try:
                existing_song = Song.objects.get(file_hash=file_hash)
                sid = existing_song.id
                
                # Optionally clear existing fingerprints to refresh them
                Fingerprint.objects.filter(song_id=sid).delete()
            except Song.DoesNotExist:
                # Insert new song
                sid = djv.db.insert_song(song_name, file_hash, len(hashes))
            
            # Insert fingerprints
            for hash_value, offset in hashes:
                djv.db.add_fingerprint(hash_value, sid, offset)
            
            # Verify fingerprints were saved
            fingerprint_count = Fingerprint.objects.filter(song_id=sid).count()
            return JsonResponse({
                'message': f'Successfully fingerprinted {song_name}',
                'hash_count': len(hashes),
                'fingerprints_stored': fingerprint_count
            })
        except Exception as e:
            import traceback
            traceback.print_exc()
            return JsonResponse({'error': str(e)}, status=500)
        finally:
            # Clean up
            if os.path.exists(temp_path):
                os.remove(temp_path)
    
    return JsonResponse({'error': 'Invalid request'}, status=400)
