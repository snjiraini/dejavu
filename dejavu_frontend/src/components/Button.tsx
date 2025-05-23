import React, { ButtonHTMLAttributes, ReactNode } from "react";
import { twMerge } from "tailwind-merge";

type ButtonVariant = "primary" | "secondary" | "tertiary" | "outline" | "link";
type ButtonSize = "sm" | "md" | "lg";

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  children: ReactNode;
  variant?: ButtonVariant;
  size?: ButtonSize;
  className?: string;
  icon?: string;
  isLoading?: boolean;
}

export const Button: React.FC<ButtonProps> = ({
  children,
  variant = "primary",
  size = "md",
  className = "",
  icon,
  isLoading = false,
  ...props
}) => {
  const baseClasses =
    "inline-flex items-center justify-center font-medium transition-colors focus:outline-none";

  const variantClasses = {
    primary: "bg-blue text-light hover:opacity-90",
    secondary: "bg-red text-light hover:opacity-90",
    tertiary: "bg-orange text-light hover:opacity-90",
    outline: "bg-transparent border border-grey text-dark hover:bg-grey",
    link: "bg-transparent text-blue hover:underline p-0",
  };

  const sizeClasses = {
    sm: "text-xs px-3 py-1.5 rounded-full",
    md: "text-sm px-4 py-2 rounded-full",
    lg: "text-base px-6 py-2.5 rounded-full",
  };

  const classes = twMerge(
    baseClasses,
    variantClasses[variant],
    sizeClasses[size],
    isLoading && "opacity-70 cursor-not-allowed",
    className
  );

  return (
    <button
      className={classes}
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
          {icon && <i className={`bx ${icon} mr-2`}></i>}
          {children}
        </>
      )}
    </button>
  );
};

export const DownloadButton: React.FC<ButtonProps> = (props) => {
  return (
    <Button
      variant="primary"
      className="h-9 px-4 py-0 rounded-[36px]"
      icon="bxs-cloud-download bx-fade-down-hover"
      {...props}
    >
      {props.children || "Download"}
    </Button>
  );
};
