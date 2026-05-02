import { cn } from "@/lib/utils";

// ── Badge ─────────────────────────────────────────────────────────────────────
interface BadgeProps {
  children: React.ReactNode;
  className?: string;
  variant?: "default" | "gold" | "green" | "red" | "stone";
}

export function Badge({ children, className, variant = "default" }: BadgeProps) {
  const variants = {
    default: "bg-stone-100 text-stone-700 border border-stone-200",
    gold: "bg-gold/15 text-gold-dark border border-gold/30",
    green: "bg-emerald-50 text-emerald-700 border border-emerald-200",
    red: "bg-red-50 text-red-600 border border-red-200",
    stone: "bg-stone-100 text-stone-500 border border-stone-200",
  };
  return (
    <span
      className={cn(
        "inline-flex items-center px-2.5 py-0.5 rounded-sm text-xs font-semibold tracking-wide",
        variants[variant],
        className
      )}
    >
      {children}
    </span>
  );
}

// ── Card ──────────────────────────────────────────────────────────────────────
interface CardProps {
  children: React.ReactNode;
  className?: string;
  hover?: boolean;
}

export function Card({ children, className, hover = false }: CardProps) {
  return (
    <div
      className={cn(
        "bg-white border border-stone-200 rounded-sm",
        hover && "transition-all hover:shadow-md hover:-translate-y-0.5 cursor-pointer",
        className
      )}
    >
      {children}
    </div>
  );
}

// ── Select ────────────────────────────────────────────────────────────────────
interface SelectProps extends React.SelectHTMLAttributes<HTMLSelectElement> {
  label?: string;
  error?: string;
  options: { value: string | number; label: string }[];
}

export function Select({ label, error, options, className, id, ...props }: SelectProps) {
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
      <select
        id={id}
        className={cn(
          "w-full rounded-sm border border-stone-300 bg-white px-4 py-2.5 text-sm text-ink transition-all",
          "focus:border-gold focus:outline-none focus:ring-2 focus:ring-gold/20",
          error && "border-red-400",
          className
        )}
        {...props}
      >
        {options.map((o) => (
          <option key={o.value} value={o.value}>
            {o.label}
          </option>
        ))}
      </select>
      {error && <p className="text-xs text-red-500">{error}</p>}
    </div>
  );
}

// ── Spinner ───────────────────────────────────────────────────────────────────
export function Spinner({ className }: { className?: string }) {
  return (
    <div
      className={cn(
        "h-8 w-8 animate-spin rounded-full border-2 border-stone-200 border-t-gold",
        className
      )}
    />
  );
}

// ── Empty State ───────────────────────────────────────────────────────────────
interface EmptyProps {
  icon?: React.ReactNode;
  title: string;
  description?: string;
  action?: React.ReactNode;
}

export function Empty({ icon, title, description, action }: EmptyProps) {
  return (
    <div className="flex flex-col items-center justify-center py-16 px-4 text-center">
      {icon && (
        <div className="mb-4 text-stone-300">{icon}</div>
      )}
      <h3 className="font-serif text-lg font-semibold text-stone-600">{title}</h3>
      {description && (
        <p className="mt-2 text-sm text-stone-400 max-w-sm">{description}</p>
      )}
      {action && <div className="mt-6">{action}</div>}
    </div>
  );
}

// ── Stars ─────────────────────────────────────────────────────────────────────
export function Stars({ count, size = 14 }: { count: number; size?: number }) {
  return (
    <span className="flex items-center gap-0.5">
      {Array.from({ length: 5 }).map((_, i) => (
        <svg
          key={i}
          width={size}
          height={size}
          viewBox="0 0 24 24"
          fill={i < count ? "#C9A84C" : "none"}
          stroke={i < count ? "#C9A84C" : "#D1C9BC"}
          strokeWidth={2}
        >
          <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2" />
        </svg>
      ))}
    </span>
  );
}
