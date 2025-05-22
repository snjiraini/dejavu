"use client";

import axiosClient from "./axiosClient";
import { Track } from "@/types";

interface TrackListResponse {
  tracks: {
    track_id: string;
    title: string;
    duration: number | null;
    isrc: string | null;
    album: string | null;
  }[];
}

interface TrackDetailResponse {
  track_id: string;
  title: string;
  duration: number | null;
  isrc: string | null;
  lyrics: string | null;
  album: {
    album_id: string;
    title: string;
  } | null;
  artists: {
    artist_id: string;
    name: string;
    role: string | null;
  }[];
  audio_files: {
    id: string;
    format: string;
    bitrate: number | null;
    path: string;
  }[];
  file_hash: string;
  total_hashes: number;
  created_at: string;
  updated_at: string;
}

// Helper function to convert API response to our frontend type
const mapTrackFromApi = (data: TrackDetailResponse): Track => {
  return {
    id: parseInt(data.track_id.split("-")[0], 16), // Convert UUID to numeric ID for frontend
    title: data.title,
    duration: data.duration || 0,
    isrc: data.isrc,
    lyrics: data.lyrics,
    created_at: data.created_at,
    updated_at: data.updated_at,
  };
};

export const trackService = {
  // Get all tracks
  async getTracks(): Promise<Track[]> {
    try {
      const response = await axiosClient.get<TrackListResponse>(
        "/api/catalog/tracks/"
      );

      // Convert to frontend Track objects
      return response.data.tracks.map((track) => ({
        id: parseInt(track.track_id.split("-")[0], 16), // Convert UUID to numeric ID for frontend
        title: track.title,
        duration: track.duration || 0,
        isrc: track.isrc,
        lyrics: null, // Not included in list response
        created_at: "", // Not included in list response
        updated_at: "", // Not included in list response
      }));
    } catch (error) {
      console.error("Error fetching tracks:", error);
      throw new Error("Failed to fetch tracks");
    }
  },

  // Get track by ID
  async getTrack(id: string): Promise<Track> {
    try {
      const response = await axiosClient.get<TrackDetailResponse>(
        `/api/catalog/tracks/${id}/`
      );
      return mapTrackFromApi(response.data);
    } catch (error) {
      console.error(`Error fetching track ${id}:`, error);
      throw new Error("Failed to fetch track");
    }
  },

  // Create a new track
  async createTrack(track: Partial<Track>): Promise<Track> {
    try {
      const response = await axiosClient.post<TrackDetailResponse>(
        "/api/catalog/tracks/",
        {
          title: track.title,
          duration: track.duration,
          isrc: track.isrc,
          lyrics: track.lyrics,
        }
      );

      return mapTrackFromApi(response.data);
    } catch (error) {
      console.error("Error creating track:", error);
      throw new Error("Failed to create track");
    }
  },

  // Update a track
  async updateTrack(id: string, track: Partial<Track>): Promise<Track> {
    try {
      const response = await axiosClient.put<TrackDetailResponse>(
        `/api/catalog/tracks/${id}/`,
        {
          title: track.title,
          duration: track.duration,
          isrc: track.isrc,
          lyrics: track.lyrics,
        }
      );

      return mapTrackFromApi(response.data);
    } catch (error) {
      console.error(`Error updating track ${id}:`, error);
      throw new Error("Failed to update track");
    }
  },

  // Delete a track
  async deleteTrack(id: string): Promise<void> {
    try {
      await axiosClient.delete(`/api/catalog/tracks/${id}/`);
    } catch (error) {
      console.error(`Error deleting track ${id}:`, error);
      throw new Error("Failed to delete track");
    }
  },
};
