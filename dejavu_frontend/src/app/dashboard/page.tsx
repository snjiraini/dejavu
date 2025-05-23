"use client";

import React, { useEffect } from "react";
import { Layout } from "@/components/Layout";
import { BoxInfo, TableData, TodoItem } from "@/components/Card";
import { DownloadButton } from "@/components/Button";
import { initAdminHub } from "@/utils/adminHub";

export default function Dashboard() {
  // Initialize AdminHub functionality
  useEffect(() => {
    initAdminHub();
  }, []);

  return (
    <Layout title="Dashboard | Dejavu Music Monitoring">
      {/* Head Title */}
      <div className="flex items-center justify-between flex-wrap gap-4 mb-9">
        <div className="left">
          <h1 className="text-4xl font-semibold mb-2.5">Dashboard</h1>
          <ul className="flex items-center gap-4">
            <li>
              <a href="#" className="text-dark">
                Dashboard
              </a>
            </li>
            <li>
              <i className="bx bx-chevron-right"></i>
            </li>
            <li>
              <a href="#" className="text-blue">
                Home
              </a>
            </li>
          </ul>
        </div>
        <DownloadButton>Get PDF</DownloadButton>
      </div>

      {/* Box Info */}
      <ul className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mt-9">
        <BoxInfo
          icon="bxs-calendar-check"
          iconColor="text-blue"
          iconBg="bg-light-blue"
          title="New Tracks"
          value={1020}
        />
        <BoxInfo
          icon="bxs-group"
          iconColor="text-yellow"
          iconBg="bg-light-yellow"
          title="Artists"
          value={2834}
        />
        <BoxInfo
          icon="bxs-dollar-circle"
          iconColor="text-orange"
          iconBg="bg-light-orange"
          title="Total Revenue"
          value="N$2543.00"
        />
      </ul>

      {/* Table Data */}
      <div className="flex flex-wrap gap-6 mt-6">
        {/* Recent Tracks */}
        <TableData
          title="Recent Tracks"
          className="flex-grow flex-basis-[500px]"
          actions={
            <div className="flex gap-2">
              <i className="bx bx-search text-xl cursor-pointer"></i>
              <i className="bx bx-filter text-xl cursor-pointer"></i>
            </div>
          }
        >
          <table className="w-full border-collapse">
            <thead>
              <tr>
                <th className="pb-3 text-left text-sm border-b border-grey">
                  Track
                </th>
                <th className="pb-3 text-left text-sm border-b border-grey">
                  Date Added
                </th>
                <th className="pb-3 text-left text-sm border-b border-grey">
                  Status
                </th>
              </tr>
            </thead>
            <tbody>
              <tr className="hover:bg-grey">
                <td className="py-4 flex items-center gap-3">
                  <div className="w-9 h-9 rounded-full bg-blue flex items-center justify-center text-light">
                    M
                  </div>
                  <p>Midnight Blues</p>
                </td>
                <td className="py-4">18-10-2023</td>
                <td className="py-4">
                  <span className="status status-completed">Approved</span>
                </td>
              </tr>
              <tr className="hover:bg-grey">
                <td className="py-4 flex items-center gap-3">
                  <div className="w-9 h-9 rounded-full bg-tertiary-500 flex items-center justify-center text-light">
                    S
                  </div>
                  <p>Summer Vibes</p>
                </td>
                <td className="py-4">01-06-2023</td>
                <td className="py-4">
                  <span className="status status-pending">Pending</span>
                </td>
              </tr>
              <tr className="hover:bg-grey">
                <td className="py-4 flex items-center gap-3">
                  <div className="w-9 h-9 rounded-full bg-secondary-500 flex items-center justify-center text-light">
                    D
                  </div>
                  <p>Desert Rose</p>
                </td>
                <td className="py-4">14-10-2023</td>
                <td className="py-4">
                  <span className="status status-process">Processing</span>
                </td>
              </tr>
              <tr className="hover:bg-grey">
                <td className="py-4 flex items-center gap-3">
                  <div className="w-9 h-9 rounded-full bg-primary-500 flex items-center justify-center text-dark">
                    R
                  </div>
                  <p>Rainy Day</p>
                </td>
                <td className="py-4">01-02-2023</td>
                <td className="py-4">
                  <span className="status status-pending">Pending</span>
                </td>
              </tr>
              <tr className="hover:bg-grey">
                <td className="py-4 flex items-center gap-3">
                  <div className="w-9 h-9 rounded-full bg-blue flex items-center justify-center text-light">
                    C
                  </div>
                  <p>City Lights</p>
                </td>
                <td className="py-4">31-10-2023</td>
                <td className="py-4">
                  <span className="status status-completed">Approved</span>
                </td>
              </tr>
            </tbody>
          </table>
        </TableData>

        {/* Todo List */}
        <TableData
          title="Todos"
          className="flex-grow flex-basis-[300px]"
          actions={
            <div className="flex gap-2">
              <i className="bx bx-plus text-xl cursor-pointer"></i>
              <i className="bx bx-filter text-xl cursor-pointer"></i>
            </div>
          }
        >
          <ul className="todo-list w-full">
            <TodoItem text="Check new track submissions" completed={true} />
            <TodoItem text="Review artist applications" completed={true} />
            <TodoItem
              text="Contact radio stations for playlist updates"
              completed={false}
            />
            <TodoItem text="Update music catalog" completed={true} />
            <TodoItem text="Analyze monthly revenue" completed={false} />
          </ul>
        </TableData>
      </div>
    </Layout>
  );
}
