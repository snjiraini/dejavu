// User and Authentication Types
export interface User {
  id: number;
  username: string;
  email: string;
  role: UserRole;
}

export enum UserRole {
  CATALOG_ADMIN = "CATALOG_ADMIN",
  RIGHTS_HOLDER = "RIGHTS_HOLDER",
  RADIO_MONITOR = "RADIO_MONITOR",
  DEVELOPER = "DEVELOPER",
  BUSINESS_ANALYST = "BUSINESS_ANALYST",
  ARTIST = "ARTIST",
}

// Core Music Catalog Types
export interface Track {
  id: number;
  title: string;
  duration: number;
  isrc: string | null;
  lyrics: string | null;
  created_at: string;
  updated_at: string;
}

export interface Album {
  id: number;
  title: string;
  release_date: string | null;
  tracks: Track[];
}

export interface Artist {
  id: number;
  name: string;
  is_group: boolean;
  members?: Artist[];
}

export interface AudioFile {
  id: number;
  track_id: number;
  format: string;
  bitrate: number;
  file_path: string;
}

// Ownership & Rights Types
export interface TrackOwnership {
  id: number;
  track_id: number;
  owner_type: "artist" | "artist_group";
  owner_id: number;
  percentage: number;
}

export interface RoyaltyShare {
  id: number;
  track_id: number;
  recipient_type: "artist" | "artist_group";
  recipient_id: number;
  percentage: number;
}

// Radio Detection Types
export interface RadioStation {
  id: number;
  name: string;
  location: string;
}

export interface RadioAirplayLog {
  id: number;
  station_id: number;
  track_id: number;
  timestamp: string;
  confidence: number;
  station?: RadioStation;
  track?: Track;
}
