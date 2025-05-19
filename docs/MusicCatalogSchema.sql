-- music_catalog_schema.sql
-- Core Music Catalog Tables

CREATE TABLE artists (
    artist_id UUID PRIMARY KEY,
    name TEXT NOT NULL,
    type TEXT CHECK (type IN ('solo', 'group')),
    bio TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE artist_groups (
    group_id UUID PRIMARY KEY,
    group_name TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE artist_group_members (
    group_id UUID REFERENCES artist_groups(group_id),
    artist_id UUID REFERENCES artists(artist_id),
    PRIMARY KEY (group_id, artist_id)
);

CREATE TABLE albums (
    album_id UUID PRIMARY KEY,
    title TEXT NOT NULL,
    release_date DATE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE tracks (
    track_id UUID PRIMARY KEY,
    title TEXT NOT NULL,
    duration INTEGER,
    isrc TEXT UNIQUE,
    lyrics TEXT,
    album_id UUID REFERENCES albums(album_id),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE track_artists (
    track_id UUID REFERENCES tracks(track_id),
    artist_id UUID REFERENCES artists(artist_id),
    role TEXT,
    PRIMARY KEY (track_id, artist_id)
);

CREATE TABLE audio_files (
    audio_file_id UUID PRIMARY KEY,
    track_id UUID REFERENCES tracks(track_id),
    format TEXT,
    bitrate INTEGER,
    storage_path TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE fingerprints (
    fingerprint_id UUID PRIMARY KEY,
    track_id UUID REFERENCES tracks(track_id),
    hash TEXT NOT NULL,
    offset INTEGER,
    date_created TIMESTAMP DEFAULT NOW(),
    date_modified TIMESTAMP DEFAULT NOW()
);

-- Ownership & Rights

CREATE TABLE track_ownerships (
    ownership_id UUID PRIMARY KEY,
    track_id UUID REFERENCES tracks(track_id),
    owner_type TEXT CHECK (owner_type IN ('artist', 'group')),
    owner_id UUID NOT NULL,
    ownership_percentage NUMERIC(5,2),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE royalty_shares (
    share_id UUID PRIMARY KEY,
    track_id UUID REFERENCES tracks(track_id),
    recipient_id UUID,
    recipient_type TEXT CHECK (recipient_type IN ('artist', 'group')),
    share_percentage NUMERIC(5,2),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Radio Detection

CREATE TABLE radio_stations (
    station_id UUID PRIMARY KEY,
    name TEXT NOT NULL,
    location TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE radio_airplay_logs (
    log_id UUID PRIMARY KEY,
    station_id UUID REFERENCES radio_stations(station_id),
    track_id UUID REFERENCES tracks(track_id),
    played_at TIMESTAMP NOT NULL,
    confidence_score NUMERIC(5,2),
    created_at TIMESTAMP DEFAULT NOW()
);

-- Notification Trigger

CREATE FUNCTION notify_airplay_match() RETURNS TRIGGER AS $$
BEGIN
    PERFORM pg_notify('airplay_alert', json_build_object(
        'track_id', NEW.track_id,
        'station_id', NEW.station_id,
        'played_at', NEW.played_at
    )::text);
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER airplay_match_trigger
AFTER INSERT ON radio_airplay_logs
FOR EACH ROW EXECUTE FUNCTION notify_airplay_match();
