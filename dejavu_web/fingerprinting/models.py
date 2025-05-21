from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

# User and Role Models
class Role(models.Model):
    """Custom roles for the system"""
    ROLE_CHOICES = [
        ('catalog_admin', 'Catalog Administrator'),
        ('rights_holder', 'Rights Holder'),
        ('radio_monitor', 'Radio Monitor'),
        ('developer', 'Developer/Engineer'),
        ('analyst', 'Business Analyst'),
        ('artist', 'Artist'),
        ('label', 'Label'),
        ('superuser', 'Super User'),
    ]
    
    name = models.CharField(max_length=20, choices=ROLE_CHOICES, unique=True)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.get_name_display()
    
    class Meta:
        db_table = 'roles'

class User(AbstractUser):
    """Extended user model with custom roles"""
    roles = models.ManyToManyField(Role, related_name='users', blank=True)
    bio = models.TextField(blank=True)
    
    # For artists/labels
    associated_artist = models.ForeignKey('Artist', null=True, blank=True, on_delete=models.SET_NULL, related_name='user_profiles')
    
    def has_role(self, role_name):
        """Check if user has a specific role"""
        return self.roles.filter(name=role_name).exists() or self.is_superuser
    
    class Meta:
        db_table = 'users'

# Create your models here.

class Artist(models.Model):
    artist_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=5, choices=[('solo', 'Solo'), ('group', 'Group')])
    bio = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'artists'

class ArtistGroup(models.Model):
    group_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    group_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.group_name

    class Meta:
        db_table = 'artist_groups'

class ArtistGroupMember(models.Model):
    group = models.ForeignKey(ArtistGroup, on_delete=models.CASCADE, to_field='group_id')
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, to_field='artist_id')

    class Meta:
        db_table = 'artist_group_members'
        unique_together = ('group', 'artist')

class Album(models.Model):
    album_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    release_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'albums'

class Track(models.Model):
    track_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    duration = models.IntegerField(null=True, blank=True)
    isrc = models.CharField(max_length=12, unique=True, null=True, blank=True)
    lyrics = models.TextField(blank=True, null=True)
    album = models.ForeignKey(Album, null=True, blank=True, on_delete=models.SET_NULL, to_field='album_id')
    
    # Keep file_hash and total_hashes for fingerprinting functionality
    file_hash = models.CharField(max_length=255, unique=True, db_index=True)
    total_hashes = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'tracks'
        indexes = [
            models.Index(fields=['file_hash']),
            models.Index(fields=['title']),
        ]

class TrackArtist(models.Model):
    track = models.ForeignKey(Track, on_delete=models.CASCADE, to_field='track_id')
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, to_field='artist_id')
    role = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        db_table = 'track_artists'
        unique_together = ('track', 'artist')

class AudioFile(models.Model):
    audio_file_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    track = models.ForeignKey(Track, on_delete=models.CASCADE, to_field='track_id')
    format = models.CharField(max_length=20)
    bitrate = models.IntegerField(null=True, blank=True)
    storage_path = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'audio_files'

class Fingerprint(models.Model):
    fingerprint_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    track = models.ForeignKey(Track, on_delete=models.CASCADE, related_name='fingerprints', to_field='track_id')
    hash = models.CharField(max_length=255, db_index=True)
    offset = models.IntegerField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'fingerprints'
        indexes = [
            models.Index(fields=['hash']),
            models.Index(fields=['track', 'offset']),
            models.Index(fields=['offset']),
        ]
        unique_together = ('hash', 'track', 'offset')

    def __str__(self):
        return f"{self.track.title} - {self.offset}"

class RadioStation(models.Model):
    station_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'radio_stations'

class RadioAirplayLog(models.Model):
    log_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    station = models.ForeignKey(RadioStation, on_delete=models.CASCADE, to_field='station_id')
    track = models.ForeignKey(Track, on_delete=models.CASCADE, to_field='track_id')
    played_at = models.DateTimeField()
    confidence_score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.station.name} - {self.track.title} - {self.played_at}"

    class Meta:
        db_table = 'radio_airplay_logs'
