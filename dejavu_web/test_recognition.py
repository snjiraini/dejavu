#!/usr/bin/env python
"""
Test script for Dejavu Django implementation
Generates samples from audio files and tests recognition
"""
import os
import sys
import json
import random
import argparse
import django
from pathlib import Path

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Add dejavu_web to sys.path for app imports
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "dejavu_web"))

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dejavu_web.settings')
django.setup()

try:
    from pydub import AudioSegment
except ImportError:
    print("Error: pydub library not found. Install with 'pip install pydub'")
    sys.exit(1)

from dejavu import Dejavu
from dejavu.logic.recognizer.file_recognizer import FileRecognizer
from fingerprinting.models import Track, Fingerprint
from dejavu.config.settings import (
    DEFAULT_FAN_VALUE,
    PEAK_NEIGHBORHOOD_SIZE,
    DEFAULT_AMP_MIN,
    PEAK_SORT,
    CONNECTIVITY_MASK
)

def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description="Test Dejavu recognition with random samples")
    parser.add_argument("--src", required=True, help="Directory containing audio files")
    parser.add_argument("--durations", nargs="+", type=int, default=[1, 2, 3, 5, 10],
                      help="Sample durations in seconds")
    parser.add_argument("--temp", required=True, help="Directory for temporary sample files")
    parser.add_argument("--results", required=True, help="Directory for results")
    parser.add_argument("--log-file", help="Log file path")
    parser.add_argument("--padding", type=int, default=8,
                      help="Padding seconds from start/end to avoid")
    parser.add_argument("--samples", type=int, default=3,
                      help="Number of samples per duration per file")
    parser.add_argument("--seed", type=int, default=42, help="Random seed")
    return parser.parse_args()

def setup_logging(log_file=None):
    """Setup logging to file and console"""
    import logging
    logger = logging.getLogger('dejavu_test')
    logger.setLevel(logging.INFO)
    
    # Create console handler
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    
    # Create formatter
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    
    # Create file handler if log file provided
    if log_file:
        fh = logging.FileHandler(log_file)
        fh.setLevel(logging.INFO)
        fh.setFormatter(formatter)
        logger.addHandler(fh)
    
    return logger

def generate_samples(source_dir, temp_dir, durations, samples_per_file, padding, logger):
    """Generate random samples from audio files"""
    # Get all audio files
    audio_files = []
    for file in os.listdir(source_dir):
        if file.endswith(".mp3") or file.endswith(".wav"):
            audio_files.append(os.path.join(source_dir, file))
    
    logger.info(f"Found {len(audio_files)} audio files in {source_dir}")
    
    # Generate samples for each file
    samples = []
    for file_path in audio_files:
        logger.info(f"Processing {file_path}...")
        try:
            # Load audio file
            audio = AudioSegment.from_file(file_path)
            
            # Get file name without extension
            base_name = os.path.splitext(os.path.basename(file_path))[0]
            
            # For each sample duration
            for duration in durations:
                duration_ms = duration * 1000  # convert to ms
                
                # Skip if audio is shorter than sample duration + padding
                if len(audio) < duration_ms + (padding * 2 * 1000):
                    logger.info(f"  Skipping {duration}s samples - audio too short")
                    continue
                    
                # Generate samples for this duration
                for i in range(samples_per_file):
                    # Choose random start position (avoiding first/last N seconds)
                    max_start = len(audio) - duration_ms - (padding * 1000)
                    min_start = padding * 1000
                    start_ms = random.randint(min_start, max_start)
                    
                    # Extract the sample
                    sample = audio[start_ms:start_ms + duration_ms]
                    
                    # Save the sample
                    sample_path = f"{temp_dir}/{base_name}_{duration}sec_{i}_start_{start_ms//1000}.mp3"
                    sample.export(sample_path, format="mp3")
                    logger.info(f"  Created {sample_path}")
                    samples.append(sample_path)
                    
        except Exception as e:
            logger.error(f"Error processing {file_path}: {e}")
    
    logger.info(f"Generated {len(samples)} samples")
    return samples

def test_recognition(sample_paths, results_dir, logger):
    """Test recognition on the generated samples"""
    # Initialize Dejavu
    config = {
        "database_type": "django",
        "models": {
            "Track": Track,
            "Fingerprint": Fingerprint
        },
        "fingerprint_limit": None,
        "peak_neighborhood_size": PEAK_NEIGHBORHOOD_SIZE,
        "fan_value": DEFAULT_FAN_VALUE,
        "amp_min": DEFAULT_AMP_MIN,
        "peak_sort": PEAK_SORT,
        "connectivity_mask": CONNECTIVITY_MASK
    }
    
    djv = Dejavu(config)
    
    results = []
    total_tests = len(sample_paths)
    correct_matches = 0
    perfect_offsets = 0
    
    # Function to extract expected track title from sample filename
    def get_expected_track(filename):
        return os.path.basename(filename).split('_')[0]
    
    logger.info(f"Testing {total_tests} samples...")
    for i, file_path in enumerate(sample_paths):
        try:
            expected_track = get_expected_track(file_path)
            duration = file_path.split('_')[1].replace('sec', '')
            start_time = int(file_path.split('_start_')[1].split('.')[0])
            
            logger.info(f"[{i+1}/{total_tests}] Testing {file_path}")
            
            # Recognize the sample
            result = djv.recognize(FileRecognizer, file_path)
            
            match_info = {
                "file": os.path.basename(file_path),
                "expected": expected_track,
                "duration": duration,
                "matched": False,
                "confidence": 0,
                "offset_accuracy": "N/A"
            }
            
            if result and 'results' in result and result['results']:
                match = result['results'][0]
                matched_track = match.get('title', b'').decode('utf-8') if isinstance(match.get('title', b''), bytes) else match.get('title', '')
                confidence = match.get('confidence', 0) if 'confidence' in match else round(match.get('input_confidence', 0) * 100, 2)
                offset_seconds = match.get('offset_seconds', 0)
                
                match_info["matched"] = True
                match_info["matched_track"] = matched_track
                match_info["confidence"] = confidence
                
                # Check if this is the correct track
                if expected_track in matched_track:
                    correct_matches += 1
                    match_info["correct"] = True
                    
                    # Check offset accuracy (how close to the expected start time)
                    offset_diff = abs(offset_seconds - start_time)
                    match_info["offset_diff"] = offset_diff
                    
                    if offset_diff <= 1:  # Within 1 second
                        perfect_offsets += 1
                        match_info["offset_accuracy"] = "Perfect"
                    elif offset_diff <= 3:  # Within 3 seconds
                        match_info["offset_accuracy"] = "Good"
                    else:
                        match_info["offset_accuracy"] = "Poor"
                else:
                    match_info["correct"] = False
            
            results.append(match_info)
            
            # Print summary for this test
            if match_info["matched"]:
                logger.info(f"  Result: Matched '{match_info.get('matched_track', 'Unknown')}' with {match_info.get('confidence', 0)}% confidence")
                logger.info(f"  Correct: {match_info.get('correct', False)}")
                if match_info.get('correct', False):
                    logger.info(f"  Offset Accuracy: {match_info.get('offset_accuracy', 'N/A')}")
            else:
                logger.info("  Result: No match found")
                
        except Exception as e:
            logger.error(f"Error testing {file_path}: {str(e)}")
            results.append({
                "file": os.path.basename(file_path),
                "error": str(e)
            })
    
    # Save results
    with open(os.path.join(results_dir, 'test_results.json'), 'w') as f:
        json.dump(results, f, indent=2)
    
    # Calculate stats
    match_rate = (correct_matches / total_tests) * 100 if total_tests > 0 else 0
    offset_accuracy = (perfect_offsets / correct_matches) * 100 if correct_matches > 0 else 0
    
    summary = {
        "total_tests": total_tests,
        "correct_matches": correct_matches,
        "match_rate": match_rate,
        "perfect_offsets": perfect_offsets,
        "offset_accuracy": offset_accuracy
    }
    
    logger.info("\nTest Summary:")
    logger.info(f"Total samples tested: {total_tests}")
    logger.info(f"Correct matches: {correct_matches} ({match_rate:.2f}%)")
    logger.info(f"Perfect offset accuracy: {perfect_offsets} ({offset_accuracy:.2f}% of correct matches)")
    
    with open(os.path.join(results_dir, 'summary.json'), 'w') as f:
        json.dump(summary, f, indent=2)
    
    logger.info(f"\nDetailed results saved to {os.path.join(results_dir, 'test_results.json')}")
    logger.info(f"Summary saved to {os.path.join(results_dir, 'summary.json')}")
    
    return results, summary

def main():
    """Main function"""
    args = parse_args()
    
    # Set random seed
    random.seed(args.seed)
    
    # Ensure directories exist
    os.makedirs(args.temp, exist_ok=True)
    os.makedirs(args.results, exist_ok=True)
    
    # Setup logging
    logger = setup_logging(args.log_file)
    
    logger.info("Dejavu Django recognition test")
    logger.info(f"Source directory: {args.src}")
    logger.info(f"Sample durations: {args.durations}")
    logger.info(f"Samples per file: {args.samples}")
    
    # Generate samples
    logger.info("\n=== Generating samples ===")
    samples = generate_samples(args.src, args.temp, args.durations, 
                              args.samples, args.padding, logger)
    
    # Test recognition
    logger.info("\n=== Testing recognition ===")
    test_recognition(samples, args.results, logger)

if __name__ == "__main__":
    main() 