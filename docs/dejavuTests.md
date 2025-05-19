# Dejavu Audio Recognition Test Scripts

This document describes the test scripts available for the Dejavu audio recognition system and how to run them.

## Available Test Scripts

### 1. `test_fingerprint.py`

This script fingerprints all audio files in a specified directory and then tests recognition against those same files.

**Purpose:** Verify that the system can accurately recognize the entire audio files that were used for fingerprinting.

**Location:** `/workspace/test_fingerprint.py`

**Usage:**

```bash
python test_fingerprint.py
```

**What it does:**

- Fingerprints all audio files in the `/workspace/mp3` directory
- Tests recognition on those same files
- Outputs recognition results including match confidence and timing offsets

**Sample Output:**

```
Fingerprinting files in /workspace/mp3...
Found 6 audio files to fingerprint.
Fingerprinting /workspace/mp3/azan_test.wav...
azan_test already fingerprinted, continuing...
Successfully fingerprinted azan_test
Fingerprinting /workspace/mp3/Brad-Sucks--Total-Breakdown.mp3...
Brad-Sucks--Total-Breakdown already fingerprinted, continuing...
Successfully fingerprinted Brad-Sucks--Total-Breakdown
Fingerprinting /workspace/mp3/Choc--Eigenvalue-Subspace-Decomposition.mp3...
Choc--Eigenvalue-Subspace-Decomposition already fingerprinted, continuing...
Successfully fingerprinted Choc--Eigenvalue-Subspace-Decomposition
Fingerprinting complete.

==================================================

Testing recognition on files in /workspace/mp3...
Found 6 audio files to test recognition.
Testing recognition on /workspace/mp3/azan_test.wav...
Recognition result for azan_test.wav:
Time taken: 8.84 seconds
  Matched: b'azan_test'
  Input confidence: 1.09
  Fingerprinted confidence: 1.09
  Offset: 0.0 seconds
Testing recognition on /workspace/mp3/Brad-Sucks--Total-Breakdown.mp3...
Recognition result for Brad-Sucks--Total-Breakdown.mp3:
Time taken: 11.36 seconds
  Matched: b'Brad-Sucks--Total-Breakdown'
  Input confidence: 1.25
  Fingerprinted confidence: 1.25
  Offset: 0.0 seconds
Recognition testing complete.
```

### 2. `test_dejavu.sh`

This shell script runs a complete fingerprinting and recognition test suite, generating random samples of different lengths from the original audio files.

**Purpose:** Test the system's ability to recognize shorter audio clips taken from random positions within the fingerprinted songs.

**Location:** `/workspace/test_dejavu.sh`

**Usage:**

```bash
# Make the script executable first (only needed once)
chmod +x test_dejavu.sh

# Run the test
./test_dejavu.sh
```

**What it does:**

- First runs the fingerprinting process on all mp3 files using `test_fingerprint.py`
- Then uses `test_recognition.py` to test recognition on random samples

**Sample Output:**

```
Fingerprinting all files in ./mp3 folder...
Fingerprinting files in /workspace/mp3...
Found 6 audio files to fingerprint.
Fingerprinting /workspace/mp3/azan_test.wav...
azan_test already fingerprinted, continuing...
Successfully fingerprinted azan_test
Fingerprinting /workspace/mp3/Brad-Sucks--Total-Breakdown.mp3...
Brad-Sucks--Total-Breakdown already fingerprinted, continuing...
Successfully fingerprinted Brad-Sucks--Total-Breakdown
...
Fingerprinting complete.

Testing recognition with random samples...
2025-05-19 13:21:36,532 - INFO - Dejavu Django recognition test
2025-05-19 13:21:36,533 - INFO - Source directory: ./mp3
2025-05-19 13:21:36,533 - INFO - Sample durations: [1, 2, 3, 5, 10]
2025-05-19 13:21:36,534 - INFO - Samples per file: 3

2025-05-19 13:21:36,534 - INFO - === Generating samples ===
2025-05-19 13:21:36,538 - INFO - Found 6 audio files in ./mp3
...
2025-05-19 13:21:41,831 - INFO - Generated 90 samples

2025-05-19 13:21:41,831 - INFO - === Testing recognition ===
2025-05-19 13:21:41,895 - INFO - Testing 90 samples...
2025-05-19 13:21:41,895 - INFO - [1/90] Testing ./temp_audio/azan_test_1sec_0_start_175.mp3
...
2025-05-19 13:22:17,234 - INFO - Total samples tested: 90
2025-05-19 13:22:17,236 - INFO - Correct matches: 89 (98.89%)
2025-05-19 13:22:17,237 - INFO - Perfect offset accuracy: 65 (73.03% of correct matches)

2025-05-19 13:22:17,258 - INFO - Detailed results saved to ./results/test_results.json
2025-05-19 13:22:17,259 - INFO - Summary saved to ./results/summary.json
Testing complete. See ./results directory for detailed results.
```

### 3. `test_recognition.py`

This Python script generates random samples from audio files and tests the recognition system on those samples.

**Purpose:** Test recognition performance on partial audio clips and generate detailed analytics.

**Location:** `/workspace/dejavu_web/test_recognition.py`

**Usage:**

```bash
python dejavu_web/test_recognition.py \
    --src ./mp3 \
    --durations 1 2 3 5 10 \
    --temp ./temp_audio \
    --results ./results \
    --log-file ./results/dejavu-test.log \
    --padding 8 \
    --samples 3 \
    --seed 42
```

**Parameters:**

- `--src`: Directory containing the source audio files
- `--durations`: Space-separated list of sample durations in seconds to test
- `--temp`: Directory for temporary sample files
- `--results`: Directory for result files
- `--log-file`: Path to save the log file
- `--padding`: Seconds to avoid at the start/end of files
- `--samples`: Number of samples per duration per file
- `--seed`: Random seed for reproducibility

**What it does:**

- Generates random sample clips from each audio file
- Tests recognition on each sample
- Calculates match rate and accuracy statistics
- Saves detailed results to JSON files

**Sample Console Output:**

```
2025-05-19 13:21:36,532 - INFO - Dejavu Django recognition test
2025-05-19 13:21:36,533 - INFO - Source directory: ./mp3
2025-05-19 13:21:36,533 - INFO - Sample durations: [1, 2, 3, 5, 10]
2025-05-19 13:21:36,534 - INFO - Samples per file: 3

2025-05-19 13:21:36,534 - INFO - === Generating samples ===
2025-05-19 13:21:36,538 - INFO - Found 6 audio files in ./mp3
2025-05-19 13:21:36,538 - INFO - Processing ./mp3/azan_test.wav...
2025-05-19 13:21:36,724 - INFO -   Created ./temp_audio/azan_test_1sec_0_start_175.mp3
2025-05-19 13:21:36,827 - INFO -   Created ./temp_audio/azan_test_1sec_1_start_37.mp3
2025-05-19 13:21:36,902 - INFO -   Created ./temp_audio/azan_test_1sec_2_start_14.mp3
...
2025-05-19 13:21:41,831 - INFO - Generated 90 samples

2025-05-19 13:21:41,831 - INFO - === Testing recognition ===
2025-05-19 13:21:41,895 - INFO - Testing 90 samples...
2025-05-19 13:21:41,895 - INFO - [1/90] Testing ./temp_audio/azan_test_1sec_0_start_175.mp3
2025-05-19 13:21:42,212 - INFO -   Result: Matched 'azan_test' with 26.0% confidence
2025-05-19 13:21:42,212 - INFO -   Correct: True
2025-05-19 13:21:42,212 - INFO -   Offset Accuracy: Poor
...
2025-05-19 13:22:17,234 - INFO - Total samples tested: 90
2025-05-19 13:22:17,236 - INFO - Correct matches: 89 (98.89%)
2025-05-19 13:22:17,237 - INFO - Perfect offset accuracy: 65 (73.03% of correct matches)

2025-05-19 13:22:17,258 - INFO - Detailed results saved to ./results/test_results.json
2025-05-19 13:22:17,259 - INFO - Summary saved to ./results/summary.json
```

**Sample Results JSON (summary.json):**

```json
{
  "total_tests": 90,
  "correct_matches": 89,
  "match_rate": 98.88888888888889,
  "perfect_offsets": 65,
  "offset_accuracy": 73.03370786516854
}
```

**Sample Results JSON (test_results.json, partial):**

```json
[
  {
    "file": "azan_test_1sec_0_start_175.mp3",
    "expected": "azan",
    "duration": "audio/azan",
    "matched": true,
    "confidence": 26.0,
    "offset_accuracy": "Poor",
    "matched_song": "azan_test",
    "correct": true,
    "offset_diff": 16.14667
  },
  {
    "file": "azan_test_1sec_1_start_37.mp3",
    "expected": "azan",
    "duration": "audio/azan",
    "matched": true,
    "confidence": 3.0,
    "offset_accuracy": "N/A",
    "matched_song": "As We Gather",
    "correct": false
  }
]
```

## Dependencies

Before running these scripts, ensure you have the required dependencies:

```bash
# Install required Python packages
pip install pydub django numpy
```

## Test Results

After running the tests, results can be found in these locations:

- **Full file recognition:** Console output from `test_fingerprint.py`
- **Random sample tests:**
  - Summary JSON: `/workspace/results/summary.json`
  - Detailed results: `/workspace/results/test_results.json`
  - Log file: `/workspace/results/dejavu-test.log`

## Test Performance

The test results summary in `testResultsSummary.md` contains detailed information about the system's recognition performance, including match rates, confidence scores, and offset accuracy.
