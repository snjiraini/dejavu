"use client";

import React from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { twMerge } from "tailwind-merge";
import { useAuth } from "@/context/AuthContext";
import { UserRole } from "@/types";
import { Button } from "./Button";

// Import icons
import {
  HomeIcon,
  MusicalNoteIcon,
  UserGroupIcon,
  DocumentTextIcon,
  RadioIcon,
  ChartBarIcon,
  CogIcon,
  WrenchScrewdriverIcon,
  BanknotesIcon,
  ArrowRightOnRectangleIcon,
} from "@heroicons/react/24/outline";

interface NavItem {
  name: string;
  href: string;
  icon: React.ForwardRefExoticComponent<React.SVGProps<SVGSVGElement>>;
  roles: UserRole[];
}

const navigation: NavItem[] = [
  {
    name: "Dashboard",
    href: "/dashboard",
    icon: HomeIcon,
    roles: Object.values(UserRole),
  },
  {
    name: "Tracks",
    href: "/tracks",
    icon: MusicalNoteIcon,
    roles: [UserRole.CATALOG_ADMIN, UserRole.RIGHTS_HOLDER, UserRole.ARTIST],
  },
  {
    name: "Artists",
    href: "/artists",
    icon: UserGroupIcon,
    roles: [UserRole.CATALOG_ADMIN, UserRole.RIGHTS_HOLDER],
  },
  {
    name: "Albums",
    href: "/albums",
    icon: DocumentTextIcon,
    roles: [UserRole.CATALOG_ADMIN, UserRole.RIGHTS_HOLDER, UserRole.ARTIST],
  },
  {
    name: "Audio Files",
    href: "/audio-files",
    icon: MusicalNoteIcon,
    roles: [UserRole.CATALOG_ADMIN, UserRole.DEVELOPER],
  },
  {
    name: "Rights & Ownership",
    href: "/rights",
    icon: BanknotesIcon,
    roles: [UserRole.RIGHTS_HOLDER, UserRole.CATALOG_ADMIN],
  },
  {
    name: "Radio Stations",
    href: "/radio-stations",
    icon: RadioIcon,
    roles: [
      UserRole.RADIO_MONITOR,
      UserRole.BUSINESS_ANALYST,
      UserRole.CATALOG_ADMIN,
    ],
  },
  {
    name: "Airplay Logs",
    href: "/airplay-logs",
    icon: RadioIcon,
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
    icon: ChartBarIcon,
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
    icon: CogIcon,
    roles: [UserRole.DEVELOPER, UserRole.CATALOG_ADMIN],
  },
  {
    name: "Developer Tools",
    href: "/developer",
    icon: WrenchScrewdriverIcon,
    roles: [UserRole.DEVELOPER],
  },
];

export const SidebarNav: React.FC = () => {
  const pathname = usePathname();
  const { user, logout, hasPermission } = useAuth();

  // Filter navigation items based on user role
  const filteredNavigation = navigation.filter(
    (item) => user && hasPermission(item.roles)
  );

  return (
    <div className="h-full flex flex-col bg-gray-50 border-r border-gray-200 w-64 shadow-soft">
      <div className="flex items-center justify-center h-16 border-b border-gray-200">
        <h1 className="text-xl font-semibold text-primary-600">Dejavu</h1>
      </div>
      <nav className="flex-1 px-2 py-4 space-y-1">
        {filteredNavigation.map((item) => {
          const isActive =
            pathname === item.href || pathname.startsWith(`${item.href}/`);

          return (
            <Link
              key={item.name}
              href={item.href}
              className={twMerge(
                "flex items-center px-3 py-2 text-sm font-medium rounded-md transition-colors",
                isActive
                  ? "bg-primary-50 text-primary-700"
                  : "text-gray-600 hover:bg-gray-100"
              )}
            >
              <item.icon
                className={twMerge(
                  "mr-3 flex-shrink-0 h-5 w-5",
                  isActive ? "text-primary-500" : "text-gray-400"
                )}
              />
              {item.name}
            </Link>
          );
        })}
      </nav>
      <div className="px-4 py-3 border-t border-gray-200">
        {user && (
          <div className="flex flex-col space-y-3">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <div className="h-8 w-8 rounded-full bg-primary-200 flex items-center justify-center text-primary-600 font-medium">
                  {user.username.charAt(0).toUpperCase()}
                </div>
              </div>
              <div className="ml-3">
                <p className="text-sm font-medium text-gray-700">
                  {user.username}
                </p>
                <p className="text-xs text-gray-500">{user.role}</p>
              </div>
            </div>
            <Button
              variant="outline"
              size="sm"
              className="w-full justify-center"
              onClick={logout}
            >
              <ArrowRightOnRectangleIcon className="h-4 w-4 mr-2" />
              Logout
            </Button>
          </div>
        )}
      </div>
    </div>
  );
};
