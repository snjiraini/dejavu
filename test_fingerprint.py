import os
import sys
import django
import time
from pathlib import Path

# Add dejavu_web to sys.path for app imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "dejavu_web"))

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dejavu_web.settings')
django.setup()

from dejavu import Dejavu
from dejavu.logic.recognizer.file_recognizer import FileRecognizer
from fingerprinting.models import Song, Fingerprint
from dejavu.config.settings import (
    DEFAULT_FAN_VALUE,
    PEAK_NEIGHBORHOOD_SIZE,
    DEFAULT_AMP_MIN,
    PEAK_SORT,
    CONNECTIVITY_MASK
)

def fingerprint_directory(directory_path):
    """Fingerprint all audio files in the given directory."""
    print(f"Fingerprinting files in {directory_path}...")
    
    # Initialize DejaVu with Django ORM
    config = {
        "database_type": "django",
        "models": {
            "Song": Song,
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
    
    # Get all audio files in the directory
    audio_extensions = ['.mp3', '.wav']
    audio_files = []
    
    for file in os.listdir(directory_path):
        file_path = os.path.join(directory_path, file)
        if os.path.isfile(file_path) and any(file.lower().endswith(ext) for ext in audio_extensions):
            audio_files.append(file_path)
    
    print(f"Found {len(audio_files)} audio files to fingerprint.")
    
    # Fingerprint each file
    for file_path in audio_files:
        try:
            print(f"Fingerprinting {file_path}...")
            song_name = os.path.splitext(os.path.basename(file_path))[0]
            djv.fingerprint_file(file_path, song_name=song_name)
            print(f"Successfully fingerprinted {song_name}")
        except Exception as e:
            print(f"Error fingerprinting {file_path}: {str(e)}")
    
    print("Fingerprinting complete.")

def test_recognition(directory_path):
    """Test recognition on all audio files in the given directory."""
    print(f"Testing recognition on files in {directory_path}...")
    
    # Initialize DejaVu with Django ORM
    config = {
        "database_type": "django",
        "models": {
            "Song": Song,
            "Fingerprint": Fingerprint
        },
        "fingerprint_limit": None,  # Process the entire file for recognition too
        "peak_neighborhood_size": PEAK_NEIGHBORHOOD_SIZE,
        "fan_value": DEFAULT_FAN_VALUE,
        "amp_min": DEFAULT_AMP_MIN,
        "peak_sort": PEAK_SORT,
        "connectivity_mask": CONNECTIVITY_MASK
    }
    
    djv = Dejavu(config)
    
    # Get all audio files in the directory
    audio_extensions = ['.mp3', '.wav']
    audio_files = []
    
    for file in os.listdir(directory_path):
        file_path = os.path.join(directory_path, file)
        if os.path.isfile(file_path) and any(file.lower().endswith(ext) for ext in audio_extensions):
            audio_files.append(file_path)
    
    print(f"Found {len(audio_files)} audio files to test recognition.")
    
    # Test recognition on each file
    results = []
    for file_path in audio_files:
        try:
            print(f"Testing recognition on {file_path}...")
            start_time = time.time()
            result = djv.recognize(FileRecognizer, file_path)
            end_time = time.time()
            
            print(f"Recognition result for {os.path.basename(file_path)}:")
            print(f"Time taken: {end_time - start_time:.2f} seconds")
            
            if result and 'results' in result and result['results']:
                for match in result['results']:
                    print(f"  Matched: {match['song_name']}")
                    print(f"  Input confidence: {match['input_confidence']}")
                    print(f"  Fingerprinted confidence: {match['fingerprinted_confidence']}")
                    print(f"  Offset: {match['offset_seconds']} seconds")
            else:
                print("  No match found")
            
            results.append({
                'file': os.path.basename(file_path),
                'result': result
            })
        except Exception as e:
            print(f"Error recognizing {file_path}: {str(e)}")
    
    print("Recognition testing complete.")
    return results

if __name__ == "__main__":
    mp3_dir = "/workspace/mp3"
    
    # First fingerprint all files
    fingerprint_directory(mp3_dir)
    
    # Then test recognition
    print("\n" + "="*50 + "\n")
    test_recognition(mp3_dir) 