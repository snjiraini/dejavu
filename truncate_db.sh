#!/bin/bash

# Script to truncate all tables in the dejavu database
# This script respects foreign key constraints and truncates tables in the correct order

echo "Truncating all tables in the dejavu database..."

# Connect to the PostgreSQL database using environment variables or defaults
DB_NAME="${DB_NAME:-dejavu}"
DB_USER="${DB_USER:-postgres}"
DB_PASSWORD="${DB_PASSWORD:-password}"
DB_HOST="${DB_HOST:-db}"
DB_PORT="${DB_PORT:-5432}"

# Export password for psql
export PGPASSWORD=$DB_PASSWORD

# Disable foreign key constraints during the operation
psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME -c "BEGIN; SET CONSTRAINTS ALL DEFERRED;"

# Truncate tables in the correct order (child tables first, then parent tables)
# This respects the foreign key dependencies between tables

echo "Truncating fingerprints table..."
psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME -c "TRUNCATE TABLE fingerprints CASCADE;"

echo "Truncating audio_files table..."
psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME -c "TRUNCATE TABLE audio_files CASCADE;"

echo "Truncating radio_airplay_logs table..."
psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME -c "TRUNCATE TABLE radio_airplay_logs CASCADE;"

echo "Truncating track_artists table..."
psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME -c "TRUNCATE TABLE track_artists CASCADE;"

echo "Truncating tracks table..."
psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME -c "TRUNCATE TABLE tracks CASCADE;"

echo "Truncating artist_group_members table..."
psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME -c "TRUNCATE TABLE artist_group_members CASCADE;"

echo "Truncating artists table..."
psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME -c "TRUNCATE TABLE artists CASCADE;"

echo "Truncating artist_groups table..."
psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME -c "TRUNCATE TABLE artist_groups CASCADE;"

echo "Truncating albums table..."
psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME -c "TRUNCATE TABLE albums CASCADE;"

echo "Truncating radio_stations table..."
psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME -c "TRUNCATE TABLE radio_stations CASCADE;"

# Re-enable foreign key constraints
psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME -c "COMMIT;"

echo "All tables truncated successfully!" 