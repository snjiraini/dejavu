import React, { InputHTMLAttributes } from "react";
import { twMerge } from "tailwind-merge";

interface InputProps extends InputHTMLAttributes<HTMLInputElement> {
  label?: string;
  error?: string;
  className?: string;
  icon?: string;
}

export const Input: React.FC<InputProps> = ({
  label,
  error,
  className,
  icon,
  ...props
}) => {
  return (
    <div className="w-full">
      {label && (
        <label className="block text-sm font-medium text-dark mb-1">
          {label}
        </label>
      )}
      <div className="relative">
        {icon && (
          <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
            <i className={`bx ${icon} text-dark-grey`}></i>
          </div>
        )}
        <input
          className={twMerge(
            "input w-full",
            icon && "pl-10",
            error && "border-red focus:border-red focus:ring-red",
            className
          )}
          {...props}
        />
      </div>
      {error && <p className="mt-1 text-xs text-red">{error}</p>}
    </div>
  );
};

interface SearchInputProps extends InputHTMLAttributes<HTMLInputElement> {
  onSearch: (query: string) => void;
  className?: string;
}

export const SearchInput: React.FC<SearchInputProps> = ({
  onSearch,
  className,
  ...props
}) => {
  const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const form = e.currentTarget;
    const formData = new FormData(form);
    const query = formData.get("search") as string;
    onSearch(query);
  };

  return (
    <form
      onSubmit={handleSubmit}
      className={twMerge("max-w-md w-full", className)}
    >
      <div className="flex items-center h-9 form-input">
        <input
          type="search"
          name="search"
          placeholder="Search..."
          className="flex-grow h-full border-none bg-grey rounded-l-full px-4 py-0 outline-none text-dark"
          {...props}
        />
        <button
          type="submit"
          className="w-9 h-full flex justify-center items-center bg-blue text-light rounded-r-full"
        >
          <i className="bx bx-search"></i>
        </button>
      </div>
    </form>
  );
};
