import { InputHTMLAttributes } from "react";
import { twMerge } from "tailwind-merge";

interface ThemeInputProps extends InputHTMLAttributes<HTMLInputElement> {
  className?: string;
}

export const ThemeInput = ({ className = "", ...props }: ThemeInputProps) => {
  return <input className={twMerge("theme-input", className)} {...props} />;
};
