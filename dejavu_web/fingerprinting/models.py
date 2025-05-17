from django.db import models

# Create your models here.

class Song(models.Model):
    song_name = models.CharField(max_length=255)
    file_hash = models.CharField(max_length=255, unique=True)  # This field will be mapped to file_sha1 in Dejavu
    total_hashes = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.song_name

    class Meta:
        db_table = 'songs'
        indexes = [
            models.Index(fields=['file_hash']),
        ]

class Fingerprint(models.Model):
    song = models.ForeignKey(Song, on_delete=models.CASCADE, related_name='fingerprints')
    hash = models.CharField(max_length=255, db_index=True)
    offset = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'fingerprints'
        indexes = [
            models.Index(fields=['hash']),
            models.Index(fields=['song', 'offset']),
        ]

    def __str__(self):
        return f"{self.song.song_name} - {self.offset}"
