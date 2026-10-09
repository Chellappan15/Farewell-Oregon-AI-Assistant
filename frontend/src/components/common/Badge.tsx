import React from "react";

export interface BadgeProps {
  children: React.ReactNode;
  variant?: "success" | "warning" | "info" | "neutral" | "primary";
  size?: "sm" | "md";
  dot?: boolean;
  className?: string;
  dotClassName?: string;
}

export const Badge: React.FC<BadgeProps> = ({
  children,
  variant = "neutral",
  size = "md",
  dot = false,
  className = "",
  dotClassName = "badge-dot",
}) => {
  return (
    <span className={`badge badge-${variant} badge-${size} ${className}`}>
      {dot && <span className={dotClassName} />}
      {children}
    </span>
  );
};

export default Badge;
