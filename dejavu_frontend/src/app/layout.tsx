import "@/styles/globals.css";
import type { Metadata } from "next";
import { AuthProvider } from "@/context/AuthContext";
import { Layout } from "@/components/Layout";

export const metadata: Metadata = {
  title: "Dejavu Music Monitoring",
  description: "Music fingerprinting and radio airplay monitoring system",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>
        <AuthProvider>
          <Layout>{children}</Layout>
        </AuthProvider>
      </body>
    </html>
  );
}
