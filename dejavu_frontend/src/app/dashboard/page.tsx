"use client";

import React, { useEffect, useState } from "react";
import { useAuth } from "@/context/AuthContext";
import { Card } from "@/components/Card";
import { UserRole } from "@/types";

export default function DashboardPage() {
  const { user, hasPermission } = useAuth();
  const [stats, setStats] = useState({
    tracks: 0,
    artists: 0,
    albums: 0,
    airplays: 0,
  });

  useEffect(() => {
    // In a real app, we would fetch actual stats from the API
    // This is just mock data for demonstration
    setStats({
      tracks: 1248,
      artists: 387,
      albums: 524,
      airplays: 34567,
    });
  }, []);

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold">Dashboard</h1>

      <div className="bg-white rounded-lg shadow-sm p-6 mb-6">
        <h2 className="text-lg font-medium mb-4">Welcome, {user?.username}!</h2>
        <p className="text-gray-600">
          You are logged in as a{" "}
          <span className="font-medium">{user?.role.replace("_", " ")}</span>
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {hasPermission([
          UserRole.CATALOG_ADMIN,
          UserRole.RIGHTS_HOLDER,
          UserRole.ARTIST,
        ]) && (
          <Card className="p-4">
            <h3 className="text-lg font-medium mb-2">Tracks</h3>
            <p className="text-3xl font-bold text-primary-600">
              {stats.tracks}
            </p>
          </Card>
        )}

        {hasPermission([UserRole.CATALOG_ADMIN, UserRole.RIGHTS_HOLDER]) && (
          <Card className="p-4">
            <h3 className="text-lg font-medium mb-2">Artists</h3>
            <p className="text-3xl font-bold text-primary-600">
              {stats.artists}
            </p>
          </Card>
        )}

        {hasPermission([
          UserRole.CATALOG_ADMIN,
          UserRole.RIGHTS_HOLDER,
          UserRole.ARTIST,
        ]) && (
          <Card className="p-4">
            <h3 className="text-lg font-medium mb-2">Albums</h3>
            <p className="text-3xl font-bold text-primary-600">
              {stats.albums}
            </p>
          </Card>
        )}

        {hasPermission([
          UserRole.RADIO_MONITOR,
          UserRole.BUSINESS_ANALYST,
          UserRole.RIGHTS_HOLDER,
        ]) && (
          <Card className="p-4">
            <h3 className="text-lg font-medium mb-2">Airplays</h3>
            <p className="text-3xl font-bold text-primary-600">
              {stats.airplays}
            </p>
          </Card>
        )}
      </div>

      <div className="mt-8">
        <h2 className="text-xl font-semibold mb-4">Quick Actions</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {hasPermission([UserRole.CATALOG_ADMIN]) && (
            <Card className="p-4 hover:bg-gray-50 cursor-pointer">
              <h3 className="text-lg font-medium">Add New Track</h3>
              <p className="text-gray-600">Upload and catalog a new track</p>
            </Card>
          )}

          {hasPermission([UserRole.RADIO_MONITOR]) && (
            <Card className="p-4 hover:bg-gray-50 cursor-pointer">
              <h3 className="text-lg font-medium">Monitor Station</h3>
              <p className="text-gray-600">Start monitoring a radio station</p>
            </Card>
          )}

          {hasPermission([
            UserRole.BUSINESS_ANALYST,
            UserRole.RIGHTS_HOLDER,
          ]) && (
            <Card className="p-4 hover:bg-gray-50 cursor-pointer">
              <h3 className="text-lg font-medium">Generate Report</h3>
              <p className="text-gray-600">Create a custom airplay report</p>
            </Card>
          )}
        </div>
      </div>
    </div>
  );
}
