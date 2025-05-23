"use client";

import React, { ReactNode, useEffect, useState } from "react";
import Head from "next/head";
import { SidebarNav } from "./SidebarNav";
import { useAuth } from "@/context/AuthContext";
import { useRouter, usePathname } from "next/navigation";

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
      <div className="flex h-screen overflow-hidden bg-bg-primary">
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
          {/* Toggle sidebar button */}
          <div className="px-6 py-3">
            <i
              className="bx bx-menu bx-sm cursor-pointer text-dark hover:bg-grey p-1.5 rounded-md transition-colors"
              onClick={toggleSidebar}
            ></i>
          </div>

          {/* Main content */}
          <main className="w-full p-4 font-poppins max-h-[calc(100vh-48px)] overflow-y-auto">
            {children}
          </main>
        </section>
      </div>
    </>
  );
};
