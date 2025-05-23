"use client";

import { useEffect, useState } from "react";

type ThemeMode = "light_mode" | "dark_mode";

export const useDarkMode = () => {
  const [themeMode, setThemeMode] = useState<ThemeMode>("dark_mode");
  const [mounted, setMounted] = useState(false);

  // Initialize theme from localStorage when component mounts or use dark mode as default
  useEffect(() => {
    setMounted(true);
    const storedTheme = localStorage.getItem("themeColor") as ThemeMode | null;
    if (storedTheme) {
      setThemeMode(storedTheme);
      applyTheme(storedTheme);
    } else {
      // Set dark mode as default if no theme is stored
      localStorage.setItem("themeColor", "dark_mode");
      applyTheme("dark_mode");
    }
  }, []);

  // Apply theme classes to body
  const applyTheme = (mode: ThemeMode) => {
    const isDarkMode = mode === "dark_mode";
    document.body.classList.toggle("theme-dark", isDarkMode);
    document.body.classList.toggle("theme-light", !isDarkMode);
  };

  // Toggle between light and dark mode
  const toggleTheme = () => {
    if (!mounted) return;
    
    const newMode = themeMode === "light_mode" ? "dark_mode" : "light_mode";
    setThemeMode(newMode);
    localStorage.setItem("themeColor", newMode);
    applyTheme(newMode);
  };

  return {
    isDarkMode: themeMode === "dark_mode",
    toggleTheme,
    mounted
  };
};
