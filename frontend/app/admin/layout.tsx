"use client";

import { useAuthStore } from "@/store/auth";
import { useRouter, usePathname } from "next/navigation";
import { useEffect } from "react";
import Link from "next/link";
import { cn } from "@/lib/utils";
import { Users, Hotel, CalendarDays, LayoutDashboard, Shield } from "lucide-react";
import { BedDouble } from "lucide-react";

const adminLinks = [
  { href: "/admin", label: "Дашборд", icon: LayoutDashboard, exact: true },
  { href: "/admin/users", label: "Пользователи", icon: Users },
  { href: "/admin/hotels", label: "Отели", icon: Hotel },
  { href: "/admin/bookings", label: "Бронирования", icon: CalendarDays },
    { href: "/admin/rooms", label: "Комнаты", icon: BedDouble },
];

export default function AdminLayout({ children }: { children: React.ReactNode }) {
  const { user, isAuth } = useAuthStore();
  const router = useRouter();
  const pathname = usePathname();

  const isAdmin = user?.role === "ADMIN" || user?.role === "S-ADMIN";

  useEffect(() => {
    if (!isAuth || !isAdmin) {
      router.push("/");
    }
  }, [isAuth, isAdmin, router]);

  if (!isAuth || !isAdmin) return null;

  return (
    <div className="flex min-h-[calc(100vh-4rem)]">
      {/* Sidebar */}
      <aside className="w-56 shrink-0 border-r border-stone-200 bg-white hidden md:block">
        <div className="p-5 border-b border-stone-100">
          <div className="flex items-center gap-2">
            <Shield size={16} className="text-gold" />
            <span className="font-semibold text-sm text-ink">Панель управления</span>
          </div>
          <p className="text-xs text-stone-400 mt-1">{user?.role}</p>
        </div>
        <nav className="p-3 space-y-1">
          {adminLinks.map(({ href, label, icon: Icon, exact }) => {
            const active = exact ? pathname === href : pathname.startsWith(href) && href !== "/admin";
            const isExactActive = exact && pathname === href;
            return (
              <Link
                key={href}
                href={href}
                className={cn(
                  "flex items-center gap-2.5 px-3 py-2 rounded-sm text-sm font-medium transition-all",
                  (isExactActive || (!exact && pathname.startsWith(href)))
                    ? "bg-ink text-cream"
                    : "text-stone-600 hover:bg-stone-100"
                )}
              >
                <Icon size={15} />
                {label}
              </Link>
            );
          })}
        </nav>
      </aside>

      {/* Content */}
      <div className="flex-1 p-6 md:p-8">{children}</div>
    </div>
  );
}
