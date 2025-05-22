"use client";

import axiosClient from "./axiosClient";
import { User } from "@/types";

interface LoginResponse {
  access: string;
  refresh: string;
}

interface UserInfoResponse {
  id: number;
  username: string;
  email: string;
  roles: string[];
  is_superuser: boolean;
}

// Map backend roles to frontend UserRole enum
const mapRoleToUserRole = (role: string): string => {
  const roleMap: Record<string, string> = {
    catalog_admin: "CATALOG_ADMIN",
    rights_holder: "RIGHTS_HOLDER",
    radio_monitor: "RADIO_MONITOR",
    developer: "DEVELOPER",
    analyst: "BUSINESS_ANALYST",
    artist: "ARTIST",
    label: "ARTIST", // Map label to ARTIST for frontend simplicity
    superuser: "CATALOG_ADMIN", // Map superuser to CATALOG_ADMIN for frontend access
  };

  return roleMap[role] || role.toUpperCase();
};

export const authService = {
  // Login with JWT
  async login(username: string, password: string): Promise<User> {
    try {
      // Get JWT token
      const tokenResponse = await axiosClient.post<LoginResponse>(
        "/api/token/",
        {
          username,
          password,
        }
      );

      // Store tokens
      localStorage.setItem("access_token", tokenResponse.data.access);
      localStorage.setItem("refresh_token", tokenResponse.data.refresh);

      // Get user info
      const userResponse = await axiosClient.get<UserInfoResponse>(
        "/api/auth/me/"
      );

      // Find the most privileged role for the frontend
      const mappedRoles = userResponse.data.roles.map(mapRoleToUserRole);
      let primaryRole = mappedRoles[0] || "ARTIST"; // Default to artist if no roles

      if (userResponse.data.is_superuser) {
        primaryRole = "CATALOG_ADMIN"; // Superusers get CATALOG_ADMIN as primary role
      }

      // Build user object
      const user: User = {
        id: userResponse.data.id,
        username: userResponse.data.username,
        email: userResponse.data.email,
        role: primaryRole as any, // Cast to UserRole enum
      };

      return user;
    } catch (error) {
      console.error("Login error:", error);
      throw new Error("Invalid credentials");
    }
  },

  // Logout
  logout(): void {
    localStorage.removeItem("access_token");
    localStorage.removeItem("refresh_token");
  },

  // Check if user is authenticated
  isAuthenticated(): boolean {
    return !!localStorage.getItem("access_token");
  },

  // Get current user info
  async getCurrentUser(): Promise<User | null> {
    try {
      if (!this.isAuthenticated()) {
        return null;
      }

      const response = await axiosClient.get<UserInfoResponse>("/api/auth/me/");

      // Find the most privileged role for the frontend
      const mappedRoles = response.data.roles.map(mapRoleToUserRole);
      let primaryRole = mappedRoles[0] || "ARTIST";

      if (response.data.is_superuser) {
        primaryRole = "CATALOG_ADMIN";
      }

      return {
        id: response.data.id,
        username: response.data.username,
        email: response.data.email,
        role: primaryRole as any, // Cast to UserRole enum
      };
    } catch (error) {
      console.error("Error fetching current user:", error);
      return null;
    }
  },
};
