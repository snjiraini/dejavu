import React, { ReactNode } from "react";
import { twMerge } from "tailwind-merge";

interface CardProps {
  className?: string;
  children: ReactNode;
}

export const Card: React.FC<CardProps> = ({ className, children }) => {
  return (
    <div className={twMerge("card rounded-xl", className)}>{children}</div>
  );
};

interface BoxInfoProps {
  icon: string;
  iconColor: string;
  iconBg: string;
  title: string;
  value: string | number;
}

export const BoxInfo: React.FC<BoxInfoProps> = ({
  icon,
  iconColor,
  iconBg,
  title,
  value,
}) => {
  // Convert any solid icons to flat versions
  const flatIcon = icon.replace("bxs-", "bx-");

  return (
    <li className="box-info-item">
      <i className={`bx ${flatIcon} box-info-icon ${iconBg} ${iconColor}`}></i>
      <span className="text">
        <h3 className="text-2xl font-semibold">{value}</h3>
        <p className="text-dark">{title}</p>
      </span>
    </li>
  );
};

interface TableDataProps {
  title: string;
  className?: string;
  children: ReactNode;
  actions?: ReactNode;
}

export const TableData: React.FC<TableDataProps> = ({
  title,
  className,
  children,
  actions,
}) => {
  return (
    <div className={twMerge("rounded-xl bg-light p-6", className)}>
      <div className="flex items-center gap-4 mb-6">
        <h3 className="text-2xl font-semibold mr-auto">{title}</h3>
        {actions}
      </div>
      {children}
    </div>
  );
};

interface TodoItemProps {
  text: string;
  completed?: boolean;
}

export const TodoItem: React.FC<TodoItemProps> = ({
  text,
  completed = false,
}) => {
  return (
    <li
      className={`w-full mb-4 bg-grey rounded-xl p-3.5 flex justify-between items-center ${
        completed
          ? "border-l-[10px] border-blue"
          : "border-l-[10px] border-orange"
      }`}
    >
      <p>{text}</p>
      <i className="bx bx-dots-vertical-rounded cursor-pointer"></i>
    </li>
  );
};
