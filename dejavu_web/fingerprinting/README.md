# Schema Migration Guide

This guide explains how to migrate to the new comprehensive music catalog schema, removing the old Song/Fingerprint models.

## Migration Steps

1. **Apply Database Migrations**

   Run the following command to apply the migration:

   ```bash
   python manage.py migrate
   ```

   This will:

   - Create the new Track model to replace Song
   - Create all the new models (Artist, Album, AudioFile, etc.)
   - Copy data from old tables to new tables
   - Set up all the required relationships
   - Add proper indexes for performance

2. **Run Data Migration Tool**

   After applying migrations, run the data migration command to set up default values:

   ```bash
   python manage.py data_migration
   ```

   This will:

   - Create default Artist and Album records
   - Create AudioFile records for existing tracks
   - Link tracks to default entities
   - Set up track-artist relationships

## About the New Schema

The new schema provides a comprehensive music catalog with:

- **Tracks, Artists, and Albums**: Standard music catalog entities
- **Fingerprinting**: Audio fingerprints for matching
- **Radio Airplay**: Track when and where music is played
- **Ownership**: Artist/group ownership and royalty tracking

## Important Changes

This migration completely replaces the old schema:

- `Song` model has been replaced with `Track`
- `song_name` is now `title`
- Relationships use UUIDs as primary keys
- All new features like artists, albums, and radio stations are included

## Testing

Run the test script to verify that fingerprinting and recognition still work:

```bash
python test_fingerprint.py
```

## Notes for Developers

The code now uses the following consistent terminology:

1. Use `Track` instead of `Song`
2. Use `title` instead of `song_name`
3. All FK relationships use the `_id` suffix
4. Access related data through these relationships:
   - `track.album.title`
   - `track.artists.all()`
   - `track.fingerprints.count()`

## Database Schema

The key tables are:

- `tracks`: Core table for audio tracks
- `artists`: Individual artists and groups
- `albums`: Collection of tracks
- `fingerprints`: Audio analysis hashes
- `audio_files`: Storage metadata
- `radio_stations`: Radio station information
- `radio_airplay_logs`: Track plays detection

User credentials summary:
Admin: username=admin, password=testpassword123
catalog_admin: username=catalog_admin, password=testpassword123
rights_holder: username=rights_holder, password=testpassword123
radio_monitor: username=radio_monitor, password=testpassword123
developer: username=developer, password=testpassword123
analyst: username=analyst, password=testpassword123
artist: username=artist, password=testpassword123
label: username=label, password=testpassword123
superuser: username=superuser, password=testpassword123
Multi-role user: username=multi_role, password=testpassword123
