"use client";

import React, { useState } from "react";
import { useRouter } from "next/navigation";
import { useAuth } from "@/context/AuthContext";
import { ThemeCard } from "@/components/ThemeCard";
import { ThemeInput } from "@/components/ThemeInput";
import { ThemeButton } from "@/components/ThemeButton";
import { ThemeHeading } from "@/components/ThemeHeading";
import { useTheme } from "@/context/ThemeContext";
import Head from "next/head";

export default function LoginPage() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const { isDarkMode, toggleTheme, mounted } = useTheme();

  const { login } = useAuth();
  const router = useRouter();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setIsLoading(true);

    try {
      await login(username, password);
      router.push("/dashboard");
    } catch (err) {
      setError("Invalid username or password");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <>
      <Head>
        <title>Login | Dejavu Music Monitoring</title>
      </Head>
      <div className="min-h-screen flex items-center justify-center bg-bg-primary py-12 px-4 sm:px-6 lg:px-8">
        <div className="max-w-md w-full space-y-8">
          <div className="flex flex-col items-center">
            <ThemeHeading as="h1" className="text-center" isGradient>
              Dejavu Music Monitoring
            </ThemeHeading>
            <ThemeHeading as="h2" className="mt-6 text-center">
              Sign in to your account
            </ThemeHeading>
            
            {/* Theme toggle button added to login page */}
            <button
              onClick={toggleTheme}
              className="theme-button mt-4"
              aria-label="Toggle theme"
            >
              <span className="material-symbols-rounded">
                {mounted && (isDarkMode ? "light_mode" : "dark_mode")}
              </span>
            </button>
          </div>
          <ThemeCard className="mt-8 p-8">
            <form className="space-y-6" onSubmit={handleSubmit}>
              <div className="space-y-4">
                <div>
                  <label
                    htmlFor="username"
                    className="block text-text-secondary text-sm mb-1"
                  >
                    Username
                  </label>
                  <ThemeInput
                    id="username"
                    name="username"
                    type="text"
                    autoComplete="username"
                    required
                    placeholder="Enter your username"
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                  />
                </div>
                <div>
                  <label
                    htmlFor="password"
                    className="block text-text-secondary text-sm mb-1"
                  >
                    Password
                  </label>
                  <ThemeInput
                    id="password"
                    name="password"
                    type="password"
                    autoComplete="current-password"
                    required
                    placeholder="Enter your password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                  />
                </div>
              </div>

              {error && (
                <div className="text-secondary-500 text-sm text-center">
                  {error}
                </div>
              )}

              <div>
                <ThemeButton
                  type="submit"
                  isLoading={isLoading}
                  isFullWidth
                  variant="text"
                  className="text-center py-3"
                >
                  Sign in
                </ThemeButton>
              </div>
            </form>
          </ThemeCard>
        </div>
      </div>
    </>
  );
}
