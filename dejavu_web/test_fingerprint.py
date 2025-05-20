import os
import sys
import django
import uuid

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dejavu_web.settings')
django.setup()

from dejavu import Dejavu
from dejavu.logic.recognizer.file_recognizer import FileRecognizer
from fingerprinting.models import Track, Fingerprint, Artist, Album, AudioFile

# Create a test file
test_file_path = '/tmp/test.wav'
with open(test_file_path, 'wb') as f:
    # Write a simple sine wave as WAV file
    import numpy as np
    from scipy.io import wavfile
    sample_rate = 44100
    duration = 5  # seconds
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    data = np.sin(2 * np.pi * 440 * t) * 32767  # 440 Hz sine wave
    wavfile.write(test_file_path, sample_rate, data.astype(np.int16))

print(f'Test file created at {test_file_path}')

# Initialize DejaVu
config = {
    'database_type': 'django',
    'models': {
        'Track': Track,  # Use Track model directly
        'Fingerprint': Fingerprint
    }
}

djv = Dejavu(config)

# Test fingerprinting
try:
    print('Attempting to fingerprint the test file...')
    # Note: Dejavu still uses song_name in its API - would need to be modified in source
    track_title, hashes, file_hash = Dejavu._fingerprint_worker((test_file_path, None), song_name='Test Track')
    print(f'Fingerprinted with {len(hashes)} hashes')
    
    # Check if track already exists with this file_hash
    existing_track = None
    try:
        existing_track = Track.objects.get(file_hash=file_hash)
        print(f'Track with this hash already exists: {existing_track.title} (ID: {existing_track.track_id})')
        track_id = existing_track.track_id
        
        # Clean up existing fingerprints for this track
        existing_fingerprints = Fingerprint.objects.filter(track_id=track_id).count()
        print(f'Found {existing_fingerprints} existing fingerprints for this track')
        if existing_fingerprints > 0:
            Fingerprint.objects.filter(track_id=track_id).delete()
            print(f'Deleted existing fingerprints for track ID {track_id}')
    except Track.DoesNotExist:
        # Create a new track directly
        track = Track.objects.create(
            track_id=uuid.uuid4(),
            title=track_title,
            file_hash=file_hash,
            total_hashes=len(hashes)
        )
        track_id = track.track_id
        print(f'Created new track with ID: {track_id}')
        
        # Create a default artist
        artist, created = Artist.objects.get_or_create(
            name="Test Artist",
            type="solo"
        )
        print(f'{"Created" if created else "Using existing"} artist: {artist.name}')
        
        # Create a default album
        album, created = Album.objects.get_or_create(
            title="Test Album"
        )
        print(f'{"Created" if created else "Using existing"} album: {album.title}')
        
        # Associate the track with the album
        track.album = album
        track.save()
        print(f'Associated track with album: {album.title}')
        
        # Create audio file record
        audio_file = AudioFile.objects.create(
            track=track,
            format='wav',
            storage_path=test_file_path
        )
        print(f'Created audio file record for track')
    
    # Insert fingerprints directly
    print(f'Inserting {len(hashes)} hashes for track ID {track_id}...')
    success_count = 0
    error_count = 0
    
    # Bulk insert fingerprints
    fingerprint_objects = []
    for i, (hash_value, offset) in enumerate(hashes):
        if i < 5:  # Just print a few for debugging
            print(f'Hash: {hash_value}, Offset: {offset}')
        try:
            fingerprint_objects.append(Fingerprint(
                track_id=track_id,
                hash=hash_value,
                offset=offset
            ))
            success_count += 1
        except Exception as e:
            print(f'Error creating fingerprint: {e}')
            error_count += 1
            if error_count > 5:  # Only show first few errors
                print("Too many errors, stopping error output...")
                break
    
    # Bulk create fingerprints
    Fingerprint.objects.bulk_create(fingerprint_objects, batch_size=1000)
    
    # Check if fingerprints were saved
    fingerprint_count = Fingerprint.objects.filter(track_id=track_id).count()
    print(f'Successfully created {success_count} out of {len(hashes)} fingerprints')
    print(f'Fingerprints in database after insertion: {fingerprint_count}')
    
    # Try to recognize the song
    print('\nTesting recognition...')
    results = djv.recognize(FileRecognizer, test_file_path)
    print(f'Recognition results: {results}')
    
except Exception as e:
    import traceback
    traceback.print_exc()
    print(f'Error: {e}') 