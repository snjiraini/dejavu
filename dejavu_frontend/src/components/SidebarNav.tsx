"use client";

import React from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { twMerge } from "tailwind-merge";
import { useAuth } from "@/context/AuthContext";
import { UserRole } from "@/types";
import { Button } from "./Button";

interface NavItem {
  name: string;
  href: string;
  icon: string;
  roles: UserRole[];
}

interface SidebarNavProps {
  hidden?: boolean;
}

const navigation: NavItem[] = [
  {
    name: "Dashboard",
    href: "/dashboard",
    icon: "bx-dashboard",
    roles: Object.values(UserRole),
  },
  {
    name: "Tracks",
    href: "/tracks",
    icon: "bx-music",
    roles: [UserRole.CATALOG_ADMIN, UserRole.RIGHTS_HOLDER, UserRole.ARTIST],
  },
  {
    name: "Artists",
    href: "/artists",
    icon: "bx-group",
    roles: [UserRole.CATALOG_ADMIN, UserRole.RIGHTS_HOLDER],
  },
  {
    name: "Albums",
    href: "/albums",
    icon: "bx-album",
    roles: [UserRole.CATALOG_ADMIN, UserRole.RIGHTS_HOLDER, UserRole.ARTIST],
  },
  {
    name: "Audio Files",
    href: "/audio-files",
    icon: "bx-file-blank",
    roles: [UserRole.CATALOG_ADMIN, UserRole.DEVELOPER],
  },
  {
    name: "Rights & Ownership",
    href: "/rights",
    icon: "bx-dollar-circle",
    roles: [UserRole.RIGHTS_HOLDER, UserRole.CATALOG_ADMIN],
  },
  {
    name: "Radio Stations",
    href: "/radio-stations",
    icon: "bx-radio",
    roles: [
      UserRole.RADIO_MONITOR,
      UserRole.BUSINESS_ANALYST,
      UserRole.CATALOG_ADMIN,
    ],
  },
  {
    name: "Airplay Logs",
    href: "/airplay-logs",
    icon: "bx-list-ul",
    roles: [
      UserRole.RADIO_MONITOR,
      UserRole.BUSINESS_ANALYST,
      UserRole.RIGHTS_HOLDER,
      UserRole.ARTIST,
      UserRole.CATALOG_ADMIN,
    ],
  },
  {
    name: "Reports",
    href: "/reports",
    icon: "bx-chart",
    roles: [
      UserRole.BUSINESS_ANALYST,
      UserRole.RIGHTS_HOLDER,
      UserRole.ARTIST,
      UserRole.CATALOG_ADMIN,
    ],
  },
  {
    name: "System Settings",
    href: "/settings",
    icon: "bx-cog",
    roles: [UserRole.DEVELOPER, UserRole.CATALOG_ADMIN],
  },
  {
    name: "Developer Tools",
    href: "/developer",
    icon: "bx-wrench",
    roles: [UserRole.DEVELOPER],
  },
];

export const SidebarNav: React.FC<SidebarNavProps> = ({ hidden = false }) => {
  const pathname = usePathname();
  const { user, logout, hasPermission } = useAuth();

  // Filter navigation items based on user role
  const filteredNavigation = navigation.filter(
    (item) => user && hasPermission(item.roles)
  );

  return (
    <section
      id="sidebar"
      className={`fixed top-0 left-0 h-full bg-light z-20 transition-all duration-300 overflow-x-hidden ${
        hidden ? "w-[60px]" : "w-[220px]"
      }`}
    >
      {/* Brand */}
      <Link
        href="/dashboard"
        className="flex items-center h-14 font-bold text-xl text-blue px-4"
      >
        <i className="bx bx-smile bx-sm min-w-[60px] flex justify-center"></i>
        <span
          className={`text transition-opacity ${
            hidden ? "opacity-0" : "opacity-100"
          }`}
        >
          Dejavu
        </span>
      </Link>

      {/* Top Menu */}
      <ul className="side-menu top w-full mt-6">
        {filteredNavigation.slice(0, -2).map((item) => {
          const isActive =
            pathname === item.href || pathname.startsWith(`${item.href}/`);

          return (
            <li
              key={item.name}
              className={`h-10 mx-1 rounded-l-xl p-1 ${
                isActive ? "active bg-grey relative" : ""
              }`}
            >
              <Link
                href={item.href}
                className={`flex items-center h-full bg-light rounded-xl text-base ${
                  isActive ? "text-blue" : "text-dark hover:text-blue"
                }`}
              >
                <i
                  className={`bx ${item.icon} min-w-[50px] flex justify-center`}
                ></i>
                <span
                  className={`text whitespace-nowrap overflow-x-hidden transition-opacity ${
                    hidden ? "opacity-0" : "opacity-100"
                  }`}
                >
                  {item.name}
                </span>
              </Link>
            </li>
          );
        })}
      </ul>

      {/* Bottom Menu */}
      <ul className="side-menu bottom w-full absolute bottom-0 left-0">
        {filteredNavigation.slice(-2).map((item, index) => {
          const isActive =
            pathname === item.href || pathname.startsWith(`${item.href}/`);

          return (
            <li
              key={item.name}
              className={`h-10 mx-1 rounded-l-xl p-1 ${
                isActive ? "active bg-grey relative" : ""
              }`}
            >
              <Link
                href={item.href}
                className={`flex items-center h-full bg-light rounded-xl text-base ${
                  isActive ? "text-blue" : "text-dark hover:text-blue"
                }`}
              >
                <i
                  className={`bx ${item.icon} ${
                    item.name === "System Settings" ? "bx-spin-hover" : ""
                  } min-w-[50px] flex justify-center`}
                ></i>
                <span
                  className={`text whitespace-nowrap overflow-x-hidden transition-opacity ${
                    hidden ? "opacity-0" : "opacity-100"
                  }`}
                >
                  {item.name}
                </span>
              </Link>
            </li>
          );
        })}

        {/* Logout */}
        <li className="h-10 mx-1 rounded-l-xl p-1">
          <a
            href="#"
            className="flex items-center h-full bg-light rounded-xl text-base text-red hover:text-red"
            onClick={(e) => {
              e.preventDefault();
              logout();
            }}
          >
            <i className="bx bx-power-off bx-burst-hover min-w-[50px] flex justify-center"></i>
            <span
              className={`text whitespace-nowrap overflow-x-hidden transition-opacity ${
                hidden ? "opacity-0" : "opacity-100"
              }`}
            >
              Logout
            </span>
          </a>
        </li>
      </ul>
    </section>
  );
};
