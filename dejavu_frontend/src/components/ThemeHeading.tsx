import { ReactNode } from "react";
import { twMerge } from "tailwind-merge";

interface ThemeHeadingProps {
  children: ReactNode;
  className?: string;
  as?: "h1" | "h2" | "h3" | "h4" | "h5" | "h6";
  isGradient?: boolean;
}

export const ThemeHeading = ({
  children,
  className = "",
  as: Component = "h1",
  isGradient = false,
}: ThemeHeadingProps) => {
  const baseClasses = "font-medium font-poppins";
  const sizeClasses = {
    h1: "text-3xl",
    h2: "text-2xl",
    h3: "text-xl",
    h4: "text-lg",
    h5: "text-base",
    h6: "text-sm",
  };

  const gradientClass = isGradient ? "bg-gradient-blue" : "text-text-primary";

  return (
    <Component
      className={twMerge(
        baseClasses,
        sizeClasses[Component],
        gradientClass,
        className
      )}
    >
      {children}
    </Component>
  );
};
