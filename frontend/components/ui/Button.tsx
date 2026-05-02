import { cn } from "@/lib/utils";
import { type ButtonHTMLAttributes, forwardRef } from "react";

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: "primary" | "secondary" | "ghost" | "danger" | "gold";
  size?: "sm" | "md" | "lg";
  loading?: boolean;
}

export const Button = forwardRef<HTMLButtonElement, ButtonProps>(
  (
    {
      className,
      variant = "primary",
      size = "md",
      loading = false,
      disabled,
      children,
      ...props
    },
    ref
  ) => {
    const base =
      "inline-flex items-center justify-center gap-2 rounded-sm font-medium transition-all focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-gold disabled:opacity-50 disabled:pointer-events-none";

    const variants = {
      primary: "bg-ink text-cream hover:bg-stone-800 active:scale-95",
      secondary:
        "border border-stone-300 bg-white text-stone-700 hover:bg-stone-50 active:scale-95",
      ghost: "text-stone-600 hover:bg-stone-100 hover:text-ink active:scale-95",
      danger: "bg-red-600 text-white hover:bg-red-700 active:scale-95",
      gold: "bg-gold text-ink hover:bg-gold-dark active:scale-95 font-semibold",
    };

    const sizes = {
      sm: "px-3 py-1.5 text-xs",
      md: "px-5 py-2.5 text-sm",
      lg: "px-7 py-3.5 text-base",
    };

    return (
      <button
        ref={ref}
        className={cn(base, variants[variant], sizes[size], className)}
        disabled={disabled || loading}
        {...props}
      >
        {loading && (
          <span className="h-4 w-4 animate-spin rounded-full border-2 border-current border-t-transparent" />
        )}
        {children}
      </button>
    );
  }
);
Button.displayName = "Button";
