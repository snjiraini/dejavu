import React from "react";
import { Card } from "@/components/Card";
import { Button } from "@/components/Button";

export default function ReportsPage() {
  // Sample report types
  const reportTypes = [
    {
      id: "artist",
      title: "Artist Performance",
      description: "Track airplay data and revenue by artist",
      icon: "📊",
    },
    {
      id: "track",
      title: "Track Analysis",
      description: "Detailed airplay history for individual tracks",
      icon: "🎵",
    },
    {
      id: "station",
      title: "Station Monitoring",
      description: "Airplay patterns by radio station and time",
      icon: "📻",
    },
    {
      id: "royalty",
      title: "Royalty Reports",
      description: "Financial reporting for royalty distributions",
      icon: "💰",
    },
    {
      id: "trend",
      title: "Trend Analysis",
      description: "Identify emerging patterns in airplay data",
      icon: "📈",
    },
    {
      id: "geographic",
      title: "Geographic Distribution",
      description: "Regional breakdown of track plays",
      icon: "🌎",
    },
  ];

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Reports</h1>
          <p className="text-gray-600 mt-1">
            Generate and download analytics reports
          </p>
        </div>
        <Button variant="secondary">Schedule Reports</Button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {reportTypes.map((report) => (
          <Card key={report.id} className="flex flex-col h-full">
            <div className="flex items-start mb-4">
              <div className="flex-shrink-0 text-2xl mr-3">{report.icon}</div>
              <div>
                <h3 className="text-lg font-medium text-gray-900">
                  {report.title}
                </h3>
                <p className="text-sm text-gray-500 mt-1">
                  {report.description}
                </p>
              </div>
            </div>
            <div className="mt-auto pt-4 flex space-x-2">
              <Button variant="outline" size="sm" className="flex-1">
                Customize
              </Button>
              <Button variant="primary" size="sm" className="flex-1">
                Generate
              </Button>
            </div>
          </Card>
        ))}
      </div>

      <Card title="Recent Reports">
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th
                  scope="col"
                  className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                >
                  Report Name
                </th>
                <th
                  scope="col"
                  className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                >
                  Type
                </th>
                <th
                  scope="col"
                  className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                >
                  Generated
                </th>
                <th
                  scope="col"
                  className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                >
                  Size
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
              <tr>
                <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                  Q3 Royalty Distribution
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  Royalty
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  Aug 15, 2023
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  1.2 MB
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                  <Button variant="outline" size="sm" className="mr-2">
                    View
                  </Button>
                  <Button variant="secondary" size="sm">
                    Download
                  </Button>
                </td>
              </tr>
              <tr>
                <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                  Monthly Station Analysis
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  Station
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  Aug 10, 2023
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  3.5 MB
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                  <Button variant="outline" size="sm" className="mr-2">
                    View
                  </Button>
                  <Button variant="secondary" size="sm">
                    Download
                  </Button>
                </td>
              </tr>
              <tr>
                <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                  Artist Performance Summary
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  Artist
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  Aug 5, 2023
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  0.8 MB
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                  <Button variant="outline" size="sm" className="mr-2">
                    View
                  </Button>
                  <Button variant="secondary" size="sm">
                    Download
                  </Button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </Card>
    </div>
  );
}
