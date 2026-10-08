import React from "react";

export interface IconButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  icon: React.ReactNode;
  label: string;
  variant?: "default" | "ghost" | "primary" | "danger";
  size?: "sm" | "md" | "lg";
  active?: boolean;
}

export const IconButton: React.FC<IconButtonProps> = ({
  icon,
  label,
  variant = "ghost",
  size = "md",
  active = false,
  disabled = false,
  className = "",
  onClick,
  ...props
}) => {
  return (
    <button
      type="button"
      title={label}
      aria-label={label}
      disabled={disabled}
      onClick={onClick}
      className={`icon-button icon-button-${variant} icon-button-${size} ${active ? "active" : ""} ${className}`}
      {...props}
    >
      {icon}
    </button>
  );
};

export default IconButton;
