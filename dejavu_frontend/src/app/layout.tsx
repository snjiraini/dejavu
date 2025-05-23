import "@/styles/globals.css";
import type { Metadata } from "next";
import { AuthProvider } from "@/context/AuthContext";
import { ThemeProvider } from "@/context/ThemeContext";
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
      <head>
        <link
          href="https://fonts.googleapis.com/css2?family=Material+Symbols+Rounded:opsz,wght,FILL,GRAD@24,400,0,0"
          rel="stylesheet"
        />
      </head>
      <body>
        <AuthProvider>
          <ThemeProvider>
            <Layout>{children}</Layout>
          </ThemeProvider>
        </AuthProvider>
      </body>
    </html>
  );
}
