"use client";

import React, { useEffect, useState } from "react";
import { Card } from "@/components/Card";
import { Button } from "@/components/Button";
import { airplayService } from "@/api/airplayService";
import { RadioAirplayLog } from "@/types";

export default function AirplayLogsPage() {
  const [airplayLogs, setAirplayLogs] = useState<RadioAirplayLog[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [filters, setFilters] = useState({
    stationId: "",
    dateRange: "7days",
    confidenceThreshold: "90",
  });

  // Fetch logs with the current filters
  useEffect(() => {
    const fetchLogs = async () => {
      try {
        setLoading(true);

        // Build filter parameters
        let startDate;
        const today = new Date();

        switch (filters.dateRange) {
          case "today":
            startDate = today.toISOString().split("T")[0];
            break;
          case "yesterday":
            const yesterday = new Date(today);
            yesterday.setDate(yesterday.getDate() - 1);
            startDate = yesterday.toISOString().split("T")[0];
            break;
          case "7days":
            const sevenDaysAgo = new Date(today);
            sevenDaysAgo.setDate(sevenDaysAgo.getDate() - 7);
            startDate = sevenDaysAgo.toISOString().split("T")[0];
            break;
          case "30days":
            const thirtyDaysAgo = new Date(today);
            thirtyDaysAgo.setDate(thirtyDaysAgo.getDate() - 30);
            startDate = thirtyDaysAgo.toISOString().split("T")[0];
            break;
          default:
            const defaultDate = new Date(today);
            defaultDate.setDate(defaultDate.getDate() - 7);
            startDate = defaultDate.toISOString().split("T")[0];
        }

        const endDate = today.toISOString().split("T")[0];

        const result = await airplayService.getAirplayLogs({
          startDate,
          endDate,
          stationId: filters.stationId || undefined,
          // Filter by confidence on the client side since the API doesn't support it directly
        });

        // Filter by confidence threshold
        const threshold = parseFloat(filters.confidenceThreshold);
        const filteredLogs = result.logs.filter(
          (log) => log.confidence >= threshold
        );

        setAirplayLogs(filteredLogs);
        setError(null);
      } catch (err) {
        console.error("Error fetching airplay logs:", err);
        setError("Failed to load airplay logs. Please try again later.");
      } finally {
        setLoading(false);
      }
    };

    fetchLogs();
  }, [filters]);

  // Handle filter changes
  const handleFilterChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    const { name, value } = e.target;
    setFilters((prev) => ({ ...prev, [name]: value }));
  };

  // Apply filters
  const handleApplyFilters = () => {
    // This will trigger the useEffect to fetch logs with new filters
    setFilters({ ...filters });
  };

  // Format date for display
  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleString();
  };

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-2xl font-bold text-gray-900">Radio Airplay Logs</h1>
        <div className="space-x-2">
          <Button variant="secondary">Export Report</Button>
          <Button variant="primary">Confirm Matches</Button>
        </div>
      </div>

      {error && (
        <div className="p-4 bg-red-50 text-red-700 rounded-md border border-red-200">
          {error}
        </div>
      )}

      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <Card className="md:col-span-1">
          <h3 className="text-lg font-medium text-gray-900 mb-4">Filters</h3>
          <div className="space-y-4">
            <div>
              <label
                htmlFor="stationId"
                className="block text-sm font-medium text-gray-700 mb-1"
              >
                Radio Station
              </label>
              <select
                id="stationId"
                name="stationId"
                value={filters.stationId}
                onChange={handleFilterChange}
                className="rounded-md border border-gray-300 w-full px-3 py-2 text-sm shadow-soft-sm focus:border-primary-500 focus:outline-none focus:ring-1 focus:ring-primary-500"
              >
                <option value="">All Stations</option>
                {/* In a real app, we would fetch this from the API */}
                <option value="1">KEXP 90.3 FM</option>
                <option value="2">WBEZ 91.5 FM</option>
                <option value="3">WXPN 88.5 FM</option>
                <option value="4">WNYC 93.9 FM</option>
                <option value="5">KCRW 89.9 FM</option>
              </select>
            </div>

            <div>
              <label
                htmlFor="dateRange"
                className="block text-sm font-medium text-gray-700 mb-1"
              >
                Date Range
              </label>
              <select
                id="dateRange"
                name="dateRange"
                value={filters.dateRange}
                onChange={handleFilterChange}
                className="rounded-md border border-gray-300 w-full px-3 py-2 text-sm shadow-soft-sm focus:border-primary-500 focus:outline-none focus:ring-1 focus:ring-primary-500"
              >
                <option value="today">Today</option>
                <option value="yesterday">Yesterday</option>
                <option value="7days">Last 7 Days</option>
                <option value="30days">Last 30 Days</option>
                <option value="custom">Custom Range</option>
              </select>
            </div>

            <div>
              <label
                htmlFor="confidenceThreshold"
                className="block text-sm font-medium text-gray-700 mb-1"
              >
                Confidence Threshold
              </label>
              <select
                id="confidenceThreshold"
                name="confidenceThreshold"
                value={filters.confidenceThreshold}
                onChange={handleFilterChange}
                className="rounded-md border border-gray-300 w-full px-3 py-2 text-sm shadow-soft-sm focus:border-primary-500 focus:outline-none focus:ring-1 focus:ring-primary-500"
              >
                <option value="90">≥ 90%</option>
                <option value="95">≥ 95%</option>
                <option value="97">≥ 97%</option>
                <option value="99">≥ 99%</option>
              </select>
            </div>

            <div className="pt-4">
              <Button
                variant="secondary"
                className="w-full"
                onClick={handleApplyFilters}
              >
                Apply Filters
              </Button>
            </div>
          </div>
        </Card>

        <Card className="md:col-span-3">
          {loading ? (
            <div className="py-12 flex justify-center">
              <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-primary-600"></div>
            </div>
          ) : airplayLogs.length === 0 ? (
            <div className="py-12 text-center text-gray-500">
              <p>No airplay logs found</p>
              <p className="mt-1 text-sm">Try adjusting your filters</p>
            </div>
          ) : (
            <div className="overflow-x-auto">
              <table className="min-w-full divide-y divide-gray-200">
                <thead className="bg-gray-50">
                  <tr>
                    <th
                      scope="col"
                      className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                    >
                      Track
                    </th>
                    <th
                      scope="col"
                      className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                    >
                      Artist
                    </th>
                    <th
                      scope="col"
                      className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                    >
                      Station
                    </th>
                    <th
                      scope="col"
                      className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                    >
                      Timestamp
                    </th>
                    <th
                      scope="col"
                      className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                    >
                      Confidence
                    </th>
                    <th
                      scope="col"
                      className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider"
                    >
                      Actions
                    </th>
                  </tr>
                </thead>
                <tbody className="bg-white divide-y divide-gray-200">
                  {airplayLogs.map((log) => (
                    <tr key={log.id}>
                      <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                        {log.track?.title || "Unknown Track"}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                        {/* Artist info might not be available */}
                        --
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                        {log.station?.name || "Unknown Station"}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                        {formatDate(log.timestamp)}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                        <span
                          className={`px-2 py-1 rounded-full text-xs ${
                            log.confidence >= 97
                              ? "bg-green-100 text-green-800"
                              : "bg-yellow-100 text-yellow-800"
                          }`}
                        >
                          {log.confidence.toFixed(1)}%
                        </span>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                        <Button variant="outline" size="sm">
                          Details
                        </Button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </Card>
      </div>
    </div>
  );
}
