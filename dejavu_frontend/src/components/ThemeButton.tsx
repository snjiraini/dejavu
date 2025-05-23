import { ButtonHTMLAttributes, ReactNode } from "react";
import { twMerge } from "tailwind-merge";

interface ThemeButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  children: ReactNode;
  className?: string;
  icon?: string;
  isCircular?: boolean;
  isFullWidth?: boolean;
  isLoading?: boolean;
  variant?: "icon" | "text";
}

export const ThemeButton = ({
  children,
  className = "",
  icon,
  isCircular = false,
  isFullWidth = false,
  isLoading = false,
  variant = "icon",
  ...props
}: ThemeButtonProps) => {
  // Determine base class based on variant and isCircular
  const baseClasses =
    isCircular || variant === "icon" ? "theme-button" : "theme-button-text";

  const widthClass = isFullWidth ? "w-full" : "";

  return (
    <button
      className={twMerge(
        baseClasses,
        widthClass,
        isLoading && "opacity-70 cursor-not-allowed",
        className
      )}
      disabled={isLoading || props.disabled}
      {...props}
    >
      {isLoading ? (
        <>
          <svg
            className="animate-spin -ml-1 mr-2 h-4 w-4"
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 24 24"
          >
            <circle
              className="opacity-25"
              cx="12"
              cy="12"
              r="10"
              stroke="currentColor"
              strokeWidth="4"
            ></circle>
            <path
              className="opacity-75"
              fill="currentColor"
              d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
            ></path>
          </svg>
          Loading...
        </>
      ) : (
        <>
          {icon &&
            (variant === "icon" ? (
              <i className={`bx ${icon}`}></i>
            ) : (
              <i className={`bx ${icon} ${children ? "mr-2" : ""}`}></i>
            ))}
          {variant === "text" || !isCircular ? children : null}
        </>
      )}
    </button>
  );
};
