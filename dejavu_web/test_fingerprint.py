import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dejavu_web.settings')
django.setup()

from dejavu import Dejavu
from dejavu.logic.recognizer.file_recognizer import FileRecognizer
from fingerprinting.models import Song, Fingerprint

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
        'Song': Song,
        'Fingerprint': Fingerprint
    }
}

djv = Dejavu(config)

# Test fingerprinting
try:
    print('Attempting to fingerprint the test file...')
    song_name, hashes, file_hash = Dejavu._fingerprint_worker((test_file_path, None), song_name='Test Song')
    print(f'Fingerprinted with {len(hashes)} hashes')
    
    # Check if song already exists with this file_hash
    existing_song = None
    try:
        existing_song = Song.objects.get(file_hash=file_hash)
        print(f'Song with this hash already exists: {existing_song.song_name} (ID: {existing_song.id})')
        sid = existing_song.id
        
        # Clean up existing fingerprints for this song
        existing_fingerprints = Fingerprint.objects.filter(song_id=sid).count()
        print(f'Found {existing_fingerprints} existing fingerprints for this song')
        if existing_fingerprints > 0:
            Fingerprint.objects.filter(song_id=sid).delete()
            print(f'Deleted existing fingerprints for song ID {sid}')
    except Song.DoesNotExist:
        # Insert into database if song doesn't exist
        sid = djv.db.insert_song(song_name, file_hash, len(hashes))
        print(f'Inserted new song with ID: {sid}')
    
    # Insert hashes
    print(f'Inserting {len(hashes)} hashes for song ID {sid}...')
    success_count = 0
    error_count = 0
    
    # Try to directly handle the insert_hashes operation
    for i, (hash_value, offset) in enumerate(hashes):
        if i < 5:  # Just print a few for debugging
            print(f'Hash: {hash_value}, Offset: {offset}')
        try:
            djv.db.add_fingerprint(hash_value, sid, offset)
            success_count += 1
        except Exception as e:
            print(f'Error adding fingerprint: {e}')
            error_count += 1
            if error_count > 5:  # Only show first few errors
                print("Too many errors, stopping error output...")
                break
    
    # Check if fingerprints were saved
    fingerprint_count = Fingerprint.objects.filter(song_id=sid).count()
    print(f'Successfully added {success_count} out of {len(hashes)} fingerprints')
    print(f'Fingerprints in database after insertion: {fingerprint_count}')
    
    # Try to recognize the song
    print('\nTesting recognition...')
    results = djv.recognize(FileRecognizer, test_file_path)
    print(f'Recognition results: {results}')
    
except Exception as e:
    import traceback
    traceback.print_exc()
    print(f'Error: {e}') 