from ..base_classes.common_database import CommonDatabase
from django.db import transaction

class DjangoDatabase(CommonDatabase):
    def __init__(self, config):
        super().__init__()
        self.Song = config['models']['Song']
        self.Fingerprint = config['models']['Fingerprint']

    def setup(self):
        """No setup needed for Django ORM"""
        pass

    def empty(self):
        """Empty the database"""
        with transaction.atomic():
            self.Fingerprint.objects.all().delete()
            self.Song.objects.all().delete()

    def delete_unfingerprinted_songs(self):
        """Delete songs that have no fingerprints"""
        with transaction.atomic():
            self.Song.objects.filter(fingerprints__isnull=True).delete()

    def get_num_songs(self):
        """Get number of songs in database"""
        return self.Song.objects.count()

    def get_songs(self):
        """Get all songs"""
        songs = self.Song.objects.all()
        # Convert Django models to dictionary format expected by Dejavu
        return [
            {
                'id': song.id,
                'song_name': song.song_name,
                'file_sha1': song.file_hash,
                'total_hashes': song.total_hashes
            }
            for song in songs
        ]

    def get_song_by_id(self, sid):
        """Get song by ID"""
        song = self.Song.objects.get(id=sid)
        # Convert Django model to dictionary format expected by Dejavu
        return {
            'id': song.id,
            'song_name': song.song_name,
            'file_sha1': song.file_hash,
            'total_hashes': song.total_hashes
        }

    def get_song_by_filehash(self, filehash):
        """Get song by filehash"""
        return self.Song.objects.get(file_hash=filehash)

    def add_song(self, song_name, file_hash, total_hashes):
        """Add a song to the database"""
        song = self.Song.objects.create(
            song_name=song_name,
            file_hash=file_hash,
            total_hashes=total_hashes
        )
        return song.id  # Return the song ID instead of the song object

    def add_fingerprint(self, hash, sid, offset):
        """Add a fingerprint to the database"""
        # Make sure sid is an integer
        if hasattr(sid, 'id'):
            # If a Song object was passed, extract its ID
            sid = sid.id
        return self.Fingerprint.objects.create(
            hash=hash,
            song_id=sid,
            offset=offset
        )

    def get_fingerprints_by_hash(self, hash):
        """Get fingerprints by hash"""
        # Ensure hash is properly formatted for searching
        print(f"Debug: Searching for fingerprints with hash: {hash}")
        fingerprints = list(self.Fingerprint.objects.filter(hash=hash))
        print(f"Debug: Found {len(fingerprints)} fingerprints for hash {hash}")
        return fingerprints

    def get_fingerprints_by_song_id(self, sid):
        """Get fingerprints by song ID"""
        return list(self.Fingerprint.objects.filter(song_id=sid))

    def get_fingerprints_by_hash_and_offset(self, hash, offset):
        """Get fingerprints by hash and offset"""
        return list(self.Fingerprint.objects.filter(hash=hash, offset=offset))

    def insert_song(self, song_name, file_hash, total_hashes=0):
        """Insert a song into the database"""
        return self.add_song(song_name, file_hash, total_hashes)

    def insert_hashes(self, sid, hashes):
        """Insert multiple hashes into the database"""
        with transaction.atomic():
            # Create fingerprint objects in bulk instead of one by one
            fingerprints = [
                self.Fingerprint(
                    hash=hash_value,
                    song_id=sid,
                    offset=offset
                ) for hash_value, offset in hashes
            ]
            
            # Use bulk_create for much faster insertion
            # This can be tuned with batch_size for very large hash sets
            batch_size = 1000
            for i in range(0, len(fingerprints), batch_size):
                self.Fingerprint.objects.bulk_create(fingerprints[i:i+batch_size])

    def set_song_fingerprinted(self, sid):
        """Mark a song as fingerprinted"""
        # In Django ORM, we don't need to explicitly mark songs as fingerprinted
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
            fingerprints = list(self.Fingerprint.objects.filter(hash__in=chunk).select_related('song'))
            all_fingerprints.extend(fingerprints)
        
        # Process the matches
        for fp in all_fingerprints:
            song_id = fp.song.id
            input_offset = offset_dict[fp.hash]
            matches.append((song_id, fp.offset - input_offset))
            
            if song_id not in dedup_hashes:
                dedup_hashes[song_id] = 1
            else:
                dedup_hashes[song_id] += 1
        
        return matches, dedup_hashes 