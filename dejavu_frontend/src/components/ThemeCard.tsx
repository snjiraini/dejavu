import { ReactNode } from "react";
import { twMerge } from "tailwind-merge";
import { useTheme } from "@/context/ThemeContext";

interface ThemeCardProps {
  children: ReactNode;
  className?: string;
}

export const ThemeCard = ({ children, className = "" }: ThemeCardProps) => {
  const { isDarkMode } = useTheme();
  
  return (
    <div className={twMerge(
      "theme-card", 
      isDarkMode ? "text-black font-medium" : "", 
      className
    )}>
      {children}
    </div>
  );
};
