"""
Data migration script for setting up relationships in the new Track schema.
This script should be run as a Django management command after applying migrations.
"""

from django.core.management.base import BaseCommand
from django.db import transaction
from fingerprinting.models import Track, Fingerprint, Artist, Album, AudioFile

class Command(BaseCommand):
    help = 'Sets up relationships for tracks in the new schema'

    def handle(self, *args, **options):
        self.stdout.write('Starting data migration for the new schema...')
        
        # 1. Create a default artist for existing tracks
        self.stdout.write('Creating default artist for existing tracks...')
        default_artist, created = Artist.objects.get_or_create(
            name='Unknown Artist',
            type='solo',
            defaults={
                'bio': 'Default artist for migrated tracks'
            }
        )
        
        # 2. Create a default album for existing tracks
        self.stdout.write('Creating default album for existing tracks...')
        default_album, created = Album.objects.get_or_create(
            title='Unknown Album',
            defaults={
                'release_date': None
            }
        )
        
        # 3. Create audio files for existing tracks
        self.stdout.write('Creating audio file records for existing tracks...')
        
        # Get all tracks
        tracks = Track.objects.all()
        self.stdout.write(f'Found {tracks.count()} tracks to migrate...')
        
        with transaction.atomic():
            for track in tracks:
                # Update track to point to default album if not set
                if not track.album:
                    track.album = default_album
                    track.save()
                
                # Create a default audio file for this track if one doesn't exist
                audio_file, created = AudioFile.objects.get_or_create(
                    track=track,
                    defaults={
                        'format': 'unknown',
                        'storage_path': f'unknown/{track.title}'
                    }
                )
                
                # Create track-artist relationship if it doesn't exist
                from fingerprinting.models import TrackArtist
                track_artist, created = TrackArtist.objects.get_or_create(
                    track=track,
                    artist=default_artist,
                    defaults={
                        'role': 'primary'
                    }
                )
                
                self.stdout.write(f'Processed track: {track.title}')
        
        self.stdout.write(self.style.SUCCESS('Migration completed successfully!'))
        self.stdout.write('Run database migrations using: python manage.py migrate') 