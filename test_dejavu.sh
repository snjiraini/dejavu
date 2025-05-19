#####################################
### Dejavu Django testing script ###
#####################################

###########
# Clear out previous results
rm -rf ./results ./temp_audio
mkdir -p ./results ./temp_audio

###########
# Fingerprint all files in the ./mp3 folder using Django implementation
echo "Fingerprinting all files in ./mp3 folder..."
python test_fingerprint.py

##########
# Run a test suite on the ./mp3 folder by extracting 1, 2, 3, 5, and 10 
# second clips sampled randomly from within each song 8 seconds 
# away from start or end, with random seed = 42
echo "Testing recognition with random samples..."
python dejavu_web/test_recognition.py \
    --src ./mp3 \
    --durations 1 2 3 5 10 \
    --temp ./temp_audio \
    --results ./results \
    --log-file ./results/dejavu-test.log \
    --padding 8 \
    --samples 3 \
    --seed 42

echo "Testing complete. See ./results directory for detailed results."
