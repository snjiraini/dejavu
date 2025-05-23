"use client";

import { createContext, useContext, ReactNode } from "react";
import { useDarkMode } from "@/hooks/useDarkMode";

type ThemeContextType = {
  isDarkMode: boolean;
  toggleTheme: () => void;
  mounted?: boolean;
};

const ThemeContext = createContext<ThemeContextType | undefined>(undefined);

export const ThemeProvider = ({ children }: { children: ReactNode }) => {
  const { isDarkMode, toggleTheme, mounted } = useDarkMode();

  return (
    <ThemeContext.Provider value={{ isDarkMode, toggleTheme, mounted }}>
      {children}
    </ThemeContext.Provider>
  );
};

export const useTheme = (): ThemeContextType => {
  const context = useContext(ThemeContext);
  if (context === undefined) {
    throw new Error("useTheme must be used within a ThemeProvider");
  }
  return context;
};
