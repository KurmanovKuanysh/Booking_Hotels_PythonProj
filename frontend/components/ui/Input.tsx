import { cn } from "@/lib/utils";
import { type InputHTMLAttributes, forwardRef } from "react";

interface InputProps extends InputHTMLAttributes<HTMLInputElement> {
  label?: string;
  error?: string;
  icon?: React.ReactNode;
}

export const Input = forwardRef<HTMLInputElement, InputProps>(
  ({ className, label, error, icon, id, ...props }, ref) => {
    return (
      <div className="flex flex-col gap-1.5">
        {label && (
          <label
            htmlFor={id}
            className="text-xs font-semibold uppercase tracking-wider text-stone-500"
          >
            {label}
          </label>
        )}
        <div className="relative">
          {icon && (
            <span className="absolute left-3 top-1/2 -translate-y-1/2 text-stone-400">
              {icon}
            </span>
          )}
          <input
            ref={ref}
            id={id}
            className={cn(
              "w-full rounded-sm border border-stone-300 bg-white px-4 py-2.5 text-sm text-ink placeholder-stone-400 transition-all",
              "focus:border-gold focus:outline-none focus:ring-2 focus:ring-gold/20",
              "disabled:bg-stone-50 disabled:cursor-not-allowed",
              error && "border-red-400 focus:border-red-400 focus:ring-red-100",
              icon && "pl-10",
              className
            )}
            {...props}
          />
        </div>
        {error && <p className="text-xs text-red-500">{error}</p>}
      </div>
    );
  }
);
Input.displayName = "Input";
