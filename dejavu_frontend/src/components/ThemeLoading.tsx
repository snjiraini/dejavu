import { twMerge } from "tailwind-merge";

interface ThemeLoadingProps {
  className?: string;
  lines?: number;
}

export const ThemeLoading = ({
  className = "",
  lines = 3,
}: ThemeLoadingProps) => {
  return (
    <div className={twMerge("flex flex-col gap-3", className)}>
      {Array.from({ length: lines }).map((_, i) => (
        <div
          key={i}
          className={`theme-loading-bar ${
            i === lines - 1 ? "w-3/4" : "w-full"
          }`}
        />
      ))}
    </div>
  );
};
