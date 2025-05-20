from ..base_classes.common_database import CommonDatabase
from django.db import transaction
from ..config.settings import FIELD_FILE_SHA1, FIELD_TOTAL_HASHES, SONG_NAME

class DjangoDatabase(CommonDatabase):
    def __init__(self, config):
        super().__init__()
        self.Track = config['models']['Track']
        self.Fingerprint = config['models']['Fingerprint']

    def setup(self):
        """No setup needed for Django ORM"""
        pass

    def empty(self):
        """Empty the database"""
        with transaction.atomic():
            self.Fingerprint.objects.all().delete()
            self.Track.objects.all().delete()

    def delete_unfingerprinted_songs(self):
        """Delete tracks that have no fingerprints"""
        with transaction.atomic():
            self.Track.objects.filter(fingerprints__isnull=True).delete()

    def get_num_songs(self):
        """Get number of tracks in database"""
        return self.Track.objects.count()

    def get_songs(self):
        """Get all tracks"""
        tracks = self.Track.objects.all()
        # Convert Django models to dictionary format expected by Dejavu
        return [
            {
                'id': track.track_id,
                SONG_NAME: track.title,
                FIELD_FILE_SHA1: track.file_hash,
                FIELD_TOTAL_HASHES: track.total_hashes
            }
            for track in tracks
        ]

    def get_song_by_id(self, track_id):
        """Get track by ID"""
        track = self.Track.objects.get(track_id=track_id)
        # Convert Django model to dictionary format expected by Dejavu
        return {
            'id': track.track_id,
            SONG_NAME: track.title,
            FIELD_FILE_SHA1: track.file_hash,
            FIELD_TOTAL_HASHES: track.total_hashes
        }

    def get_song_by_filehash(self, filehash):
        """Get track by filehash"""
        return self.Track.objects.get(file_hash=filehash)

    def add_song(self, title, file_hash, total_hashes):
        """Add a track to the database"""
        track = self.Track.objects.create(
            title=title,
            file_hash=file_hash,
            total_hashes=total_hashes
        )
        return track.track_id  # Return the track ID instead of the track object

    def add_fingerprint(self, hash, track_id, offset):
        """Add a fingerprint to the database"""
        # Make sure track_id is a valid identifier
        if hasattr(track_id, 'track_id'):
            # If a Track object was passed, extract its ID
            track_id = track_id.track_id
        return self.Fingerprint.objects.create(
            hash=hash,
            track_id=track_id,
            offset=offset
        )

    def get_fingerprints_by_hash(self, hash):
        """Get fingerprints by hash"""
        # Ensure hash is properly formatted for searching
        print(f"Debug: Searching for fingerprints with hash: {hash}")
        fingerprints = list(self.Fingerprint.objects.filter(hash=hash))
        print(f"Debug: Found {len(fingerprints)} fingerprints for hash {hash}")
        return fingerprints

    def get_fingerprints_by_song_id(self, track_id):
        """Get fingerprints by track ID"""
        return list(self.Fingerprint.objects.filter(track_id=track_id))

    def get_fingerprints_by_hash_and_offset(self, hash, offset):
        """Get fingerprints by hash and offset"""
        return list(self.Fingerprint.objects.filter(hash=hash, offset=offset))

    def insert_song(self, title, file_hash, total_hashes=0):
        """Insert a track into the database"""
        return self.add_song(title, file_hash, total_hashes)

    def insert_hashes(self, track_id, hashes):
        """Insert multiple hashes into the database"""
        with transaction.atomic():
            # Create fingerprint objects in bulk instead of one by one
            fingerprints = [
                self.Fingerprint(
                    hash=hash_value,
                    track_id=track_id,
                    offset=offset
                ) for hash_value, offset in hashes
            ]
            
            # Use bulk_create for much faster insertion
            # This can be tuned with batch_size for very large hash sets
            batch_size = 1000
            for i in range(0, len(fingerprints), batch_size):
                self.Fingerprint.objects.bulk_create(fingerprints[i:i+batch_size])

    def set_song_fingerprinted(self, track_id):
        """Mark a track as fingerprinted"""
        # In Django ORM, we don't need to explicitly mark tracks as fingerprinted
        # since we can query based on the presence of fingerprints
        pass

    def return_matches(self, hashes):
        """Return matches for the given hashes using an optimized approach"""
        matches = []
        dedup_hashes = {}
        
        # Group hashes for efficient querying
        hash_values = [hash_value for hash_value, _ in hashes]
        offset_dict = {hash_value: offset for hash_value, offset in hashes}
        
        # Use a single query with __in for much better performance
        # Split into chunks to avoid query size limits
        chunk_size = 500
        all_fingerprints = []
        
        for i in range(0, len(hash_values), chunk_size):
            chunk = hash_values[i:i+chunk_size]
            fingerprints = list(self.Fingerprint.objects.filter(hash__in=chunk).select_related('track'))
            all_fingerprints.extend(fingerprints)
        
        # Process the matches
        for fp in all_fingerprints:
            track_id = fp.track.track_id
            input_offset = offset_dict[fp.hash]
            matches.append((track_id, fp.offset - input_offset))
            
            if track_id not in dedup_hashes:
                dedup_hashes[track_id] = 1
            else:
                dedup_hashes[track_id] += 1
        
        return matches, dedup_hashes 