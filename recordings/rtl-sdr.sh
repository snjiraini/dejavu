#!/bin/bash

# Define the base filename and extension
base_filename="Hot96fm"
extension=".mp3"

# Define the duration for each segment in seconds
segment_duration=10

# Loop infinitely
while true; do
    # Generate a timestamp for the filename
    timestamp=$(date +"%Y%m%d%H%M%S")

    # Construct the filename with timestamp
    filename="${base_filename}_${timestamp}${extension}"

    # Run ffmpeg to save the RTP stream to the filename
    ffmpeg -i rtp://224.0.0.1:5004 -acodec copy -vn -t $segment_duration "$filename"

    # Sleep for the duration of the segment
    sleep $segment_duration
done
