"use client";

import axiosClient from "./axiosClient";
import { RadioAirplayLog } from "@/types";

interface AirplayLogResponse {
  logs: {
    log_id: string;
    track: {
      track_id: string;
      title: string;
    };
    station: {
      station_id: string;
      name: string;
      location: string;
    };
    played_at: string;
    confidence_score: number | null;
  }[];
  total: number;
  page: number;
  page_size: number;
}

interface AirplayLogDetailResponse {
  log_id: string;
  track: {
    track_id: string;
    title: string;
  };
  station: {
    station_id: string;
    name: string;
    location: string;
  };
  played_at: string;
  confidence_score: number | null;
  created_at: string;
}

// Helper function to convert API response to our frontend type
const mapAirplayLogFromApi = (
  data: AirplayLogDetailResponse | AirplayLogResponse["logs"][0]
): RadioAirplayLog => {
  return {
    id: parseInt(data.log_id.split("-")[0], 16), // Convert UUID to numeric ID for frontend
    station_id: parseInt(data.station.station_id.split("-")[0], 16),
    track_id: parseInt(data.track.track_id.split("-")[0], 16),
    timestamp: data.played_at,
    confidence: data.confidence_score || 0,
    station: {
      id: parseInt(data.station.station_id.split("-")[0], 16),
      name: data.station.name,
      location: data.station.location,
    },
    track: {
      id: parseInt(data.track.track_id.split("-")[0], 16),
      title: data.track.title,
      duration: 0, // Not included in the response
      isrc: null, // Not included in the response
      lyrics: null, // Not included in the response
      created_at: "", // Not included in the response
      updated_at: "", // Not included in the response
    },
  };
};

export const airplayService = {
  // Get airplay logs with optional filtering
  async getAirplayLogs(filters?: {
    startDate?: string;
    endDate?: string;
    stationId?: string;
    trackId?: string;
    page?: number;
    pageSize?: number;
  }): Promise<{
    logs: RadioAirplayLog[];
    total: number;
    page: number;
    pageSize: number;
  }> {
    try {
      // Build query parameters
      const params = new URLSearchParams();
      if (filters?.startDate) params.append("start_date", filters.startDate);
      if (filters?.endDate) params.append("end_date", filters.endDate);
      if (filters?.stationId) params.append("station_id", filters.stationId);
      if (filters?.trackId) params.append("track_id", filters.trackId);
      if (filters?.page) params.append("page", filters.page.toString());
      if (filters?.pageSize)
        params.append("page_size", filters.pageSize.toString());

      const response = await axiosClient.get<AirplayLogResponse>(
        `/api/monitoring/airplay-logs/?${params.toString()}`
      );

      // Convert to frontend objects
      const logs = response.data.logs.map((log) => mapAirplayLogFromApi(log));

      return {
        logs,
        total: response.data.total,
        page: response.data.page,
        pageSize: response.data.page_size,
      };
    } catch (error) {
      console.error("Error fetching airplay logs:", error);
      throw new Error("Failed to fetch airplay logs");
    }
  },

  // Get a specific airplay log
  async getAirplayLog(id: string): Promise<RadioAirplayLog> {
    try {
      const response = await axiosClient.get<AirplayLogDetailResponse>(
        `/api/monitoring/airplay-logs/${id}/`
      );
      return mapAirplayLogFromApi(response.data);
    } catch (error) {
      console.error(`Error fetching airplay log ${id}:`, error);
      throw new Error("Failed to fetch airplay log");
    }
  },

  // Create a new airplay log (for radio monitors)
  async createAirplayLog(log: {
    track_id: string;
    station_id: string;
    played_at: string;
    confidence_score?: number;
  }): Promise<RadioAirplayLog> {
    try {
      const response = await axiosClient.post<AirplayLogDetailResponse>(
        "/api/monitoring/airplay-logs/create/",
        log
      );
      return mapAirplayLogFromApi(response.data);
    } catch (error) {
      console.error("Error creating airplay log:", error);
      throw new Error("Failed to create airplay log");
    }
  },

  // Delete an airplay log (for radio monitors)
  async deleteAirplayLog(id: string): Promise<void> {
    try {
      await axiosClient.delete(`/api/monitoring/airplay-logs/${id}/delete/`);
    } catch (error) {
      console.error(`Error deleting airplay log ${id}:`, error);
      throw new Error("Failed to delete airplay log");
    }
  },
};
