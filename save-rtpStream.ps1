# Define the base filename and extension
$baseFilename = "Hot96fm"
$extension = ".mp3"

# Define the duration for each segment in seconds
$segmentDuration = 10

# Loop infinitely
while ($true) {
    # Generate a timestamp for the filename
    $timestamp = Get-Date -Format "yyyyMMddHHmmss"

    # Construct the filename with timestamp
    $filename = "{0}_{1}{2}" -f $baseFilename, $timestamp, $extension

    # Run ffmpeg to save the RTP stream to the filename
    ffmpeg -i "rtp://224.0.0.1:5004" -acodec copy -vn -t $segmentDuration $filename

    # Sleep for the duration of the segment
    Start-Sleep -Seconds $segmentDuration
}
