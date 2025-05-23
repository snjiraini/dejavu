"use client";

import React, { ReactNode, useEffect, useState } from "react";
import Head from "next/head";
import { SidebarNav } from "./SidebarNav";
import { useAuth } from "@/context/AuthContext";
import { useRouter, usePathname } from "next/navigation";
import {
  toggleDarkMode,
  toggleNotificationMenu,
  toggleProfileMenu,
} from "@/utils/adminHub";

interface LayoutProps {
  children: ReactNode;
  title?: string;
}

export const Layout: React.FC<LayoutProps> = ({
  children,
  title = "Dejavu Music Monitoring",
}) => {
  const { isAuthenticated, loading } = useAuth();
  const router = useRouter();
  const pathname = usePathname();
  const [sidebarHidden, setSidebarHidden] = useState(false);
  const [isDarkMode, setIsDarkMode] = useState(false);

  // Initialize dark mode state from localStorage
  useEffect(() => {
    const savedDarkMode = localStorage.getItem("darkMode") === "true";
    setIsDarkMode(savedDarkMode);
    if (savedDarkMode) {
      document.body.classList.add("dark");
    } else {
      document.body.classList.remove("dark");
    }
  }, []);

  // If not authenticated and not on the login page, redirect to login
  useEffect(() => {
    if (!loading && !isAuthenticated && pathname !== "/login") {
      router.push("/login");
    }
  }, [isAuthenticated, loading, router, pathname]);

  // Handle sidebar toggle
  const toggleSidebar = () => {
    setSidebarHidden(!sidebarHidden);
  };

  // Handle dark mode toggle
  const handleDarkModeToggle = () => {
    toggleDarkMode();
    setIsDarkMode(!isDarkMode);
  };

  // If loading, show a loading spinner
  if (loading) {
    return (
      <div className="flex h-screen items-center justify-center bg-bg-primary">
        <div className="h-8 w-8 animate-spin rounded-full border-b-2 border-t-2 border-blue"></div>
      </div>
    );
  }

  // If on login page or not authenticated, don't show sidebar
  if (pathname === "/login" || !isAuthenticated) {
    return (
      <>
        <Head>
          <title>{title}</title>
          <meta name="description" content="Dejavu Music Monitoring System" />
          <link rel="icon" href="/favicon.ico" />
          <link
            href="https://unpkg.com/boxicons@2.1.4/css/boxicons.min.css"
            rel="stylesheet"
          />
        </Head>
        <main className="min-h-screen bg-bg-primary">{children}</main>
      </>
    );
  }

  // Main layout with sidebar for authenticated users
  return (
    <>
      <Head>
        <title>{title}</title>
        <meta name="description" content="Dejavu Music Monitoring System" />
        <link rel="icon" href="/favicon.ico" />
        <link
          href="https://unpkg.com/boxicons@2.1.4/css/boxicons.min.css"
          rel="stylesheet"
        />
      </Head>
      <div
        className={`flex h-screen overflow-hidden bg-bg-primary ${
          isDarkMode ? "dark" : ""
        }`}
      >
        {/* Sidebar */}
        <SidebarNav hidden={sidebarHidden} />

        {/* Content */}
        <section
          id="content"
          className={`relative ${
            sidebarHidden
              ? "w-[calc(100%-60px)] left-[60px]"
              : "w-[calc(100%-220px)] left-[220px]"
          } transition-all duration-300`}
        >
          {/* Navbar */}
          <nav className="flex h-14 items-center justify-between bg-light px-6 sticky top-0 z-10 shadow-sm">
            {/* Menu toggle */}
            <div className="flex items-center">
              <i
                className="bx bx-menu bx-sm cursor-pointer text-dark hover:bg-grey p-1.5 rounded-md transition-colors"
                onClick={toggleSidebar}
              ></i>
              <a href="#" className="nav-link ml-6 hidden md:block text-dark">
                Categories
              </a>
            </div>

            {/* Right section */}
            <div className="flex items-center gap-4">
              {/* Dark mode switch */}
              <div className="relative">
                <input
                  type="checkbox"
                  id="switch-mode"
                  className="hidden"
                  checked={isDarkMode}
                  onChange={handleDarkModeToggle}
                />
                <label
                  htmlFor="switch-mode"
                  className="flex items-center justify-between bg-grey rounded-full w-11 h-5 p-1 cursor-pointer relative"
                >
                  <i className="bx bxs-moon text-yellow"></i>
                  <i className="bx bx-sun text-orange"></i>
                  <div
                    className={`absolute top-0.5 left-0.5 bg-blue h-4 w-4 rounded-full transition-transform ${
                      isDarkMode ? "translate-x-6" : ""
                    }`}
                  ></div>
                </label>
              </div>

              {/* Notification */}
              <div className="relative">
                <a
                  href="#"
                  className="text-dark text-xl relative"
                  onClick={(e) => {
                    e.preventDefault();
                    toggleNotificationMenu();
                  }}
                >
                  <i className="bx bxs-bell"></i>
                  <span className="absolute -top-1.5 -right-1.5 flex items-center justify-center w-5 h-5 bg-red text-light text-xs font-bold rounded-full border-2 border-light">
                    8
                  </span>
                </a>
                <div className="notification-menu">
                  <ul>
                    <li>New track submission received</li>
                    <li>Artist profile updated</li>
                    <li>New airplay detected</li>
                    <li>System update available</li>
                    <li>Reminder: Generate monthly report</li>
                  </ul>
                </div>
              </div>

              {/* Profile */}
              <div className="relative">
                <a
                  href="#"
                  className="block"
                  onClick={(e) => {
                    e.preventDefault();
                    toggleProfileMenu();
                  }}
                >
                  <div className="w-9 h-9 rounded-full bg-secondary-500 flex items-center justify-center text-white overflow-hidden">
                    {/* User avatar or initial */}
                    <span>U</span>
                  </div>
                </a>
                <div className="profile-menu">
                  <ul>
                    <li>
                      <a href="#">My Profile</a>
                    </li>
                    <li>
                      <a href="#">Settings</a>
                    </li>
                    <li>
                      <a
                        href="#"
                        onClick={(e) => {
                          e.preventDefault();
                          useAuth().logout();
                        }}
                      >
                        Log Out
                      </a>
                    </li>
                  </ul>
                </div>
              </div>
            </div>
          </nav>

          {/* Main content */}
          <main className="w-full p-4 font-poppins max-h-[calc(100vh-56px)] overflow-y-auto">
            {children}
          </main>
        </section>
      </div>
    </>
  );
};
