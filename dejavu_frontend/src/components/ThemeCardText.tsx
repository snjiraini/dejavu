import { ReactNode } from "react";
import { twMerge } from "tailwind-merge";
import { useTheme } from "@/context/ThemeContext";

interface ThemeCardTextProps {
  children: ReactNode;
  className?: string;
  as?: "p" | "h1" | "h2" | "h3" | "h4" | "h5" | "h6" | "span" | "div";
}

export const ThemeCardText = ({ 
  children, 
  className = "", 
  as: Component = "p" 
}: ThemeCardTextProps) => {
  const { isDarkMode } = useTheme();
  
  return (
    <Component 
      className={twMerge(
        isDarkMode ? "text-black font-medium" : "", 
        className
      )}
    >
      {children}
    </Component>
  );
};
