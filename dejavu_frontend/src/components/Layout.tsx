"use client";

import React, { ReactNode, useEffect } from "react";
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

  // If not authenticated and not on the login page, redirect to login
  useEffect(() => {
    if (!loading && !isAuthenticated && pathname !== "/login") {
      router.push("/login");
    }
  }, [isAuthenticated, loading, router, pathname]);

  // If loading, show a loading spinner
  if (loading) {
    return (
      <div className="flex h-screen items-center justify-center">
        <div className="h-8 w-8 animate-spin rounded-full border-b-2 border-t-2 border-primary-600"></div>
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
        </Head>
        <main className="min-h-screen bg-gray-50">{children}</main>
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
      </Head>
      <div className="flex h-screen overflow-hidden">
        {/* Sidebar */}
        <SidebarNav />

        {/* Main content */}
        <main className="flex-1 overflow-auto bg-gray-50 p-6">{children}</main>
      </div>
    </>
  );
};
