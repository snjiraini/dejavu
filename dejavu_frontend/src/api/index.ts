// Export all API services from this file for easier imports
import axiosClient from "./axiosClient";
import { authService } from "./authService";
import { trackService } from "./trackService";
import { airplayService } from "./airplayService";

// Re-export everything
export { axiosClient, authService, trackService, airplayService };

// Default export for convenience
export default {
  auth: authService,
  tracks: trackService,
  airplay: airplayService,
};
