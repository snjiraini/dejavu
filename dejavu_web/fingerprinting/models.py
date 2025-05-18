from django.db import models

# Create your models here.

class Song(models.Model):
    song_name = models.CharField(max_length=255)
    file_hash = models.CharField(max_length=255, unique=True, db_index=True)  # Add explicit db_index
    total_hashes = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.song_name

    class Meta:
        db_table = 'songs'
        indexes = [
            models.Index(fields=['file_hash']),
            # Add index for song_name for faster lookups
            models.Index(fields=['song_name']),
        ]

class Fingerprint(models.Model):
    song = models.ForeignKey(Song, on_delete=models.CASCADE, related_name='fingerprints')
    hash = models.CharField(max_length=255, db_index=True)  # Ensure this is indexed
    offset = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'fingerprints'
        indexes = [
            models.Index(fields=['hash']),
            models.Index(fields=['song', 'offset']),
            # Add an index for just the offset
            models.Index(fields=['offset']),
        ]
        # Add a compound index for better query performance
        unique_together = ('hash', 'song', 'offset')

    def __str__(self):
        return f"{self.song.song_name} - {self.offset}"
