"use client";

import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";
import { useState } from "react";
import { cn } from "@/lib/utils";
import { useAuthStore } from "@/store/auth";
import { authApi } from "@/lib/services";
import toast from "react-hot-toast";
import {
  Hotel,
  CalendarDays,
  User,
  LogOut,
  Menu,
  X,
  Shield,
  Sparkles,
} from "lucide-react";

const navLinks = [
  { href: "/hotels", label: "Отели", icon: Hotel },
  { href: "/bookings", label: "Бронирования", icon: CalendarDays, auth: true },
  { href: "/profile", label: "Профиль", icon: User, auth: true },
];

export function Navbar() {
  const pathname = usePathname();
  const router = useRouter();
  const { user, isAuth, logout, refreshToken } = useAuthStore();
  const [mobileOpen, setMobileOpen] = useState(false);

  const handleLogout = async () => {
    try {
      if (refreshToken) await authApi.logout(refreshToken);
    } catch {}
    logout();
    router.push("/");
    toast.success("До свидания!");
  };

  const isAdmin = user?.role === "ADMIN" || user?.role === "S-ADMIN";

  return (
    <nav className="sticky top-0 z-50 border-b border-stone-200 bg-cream/90 backdrop-blur-md">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div className="flex h-16 items-center justify-between">
          {/* Logo */}
          <Link href="/" className="flex items-center gap-2 group">
            <div className="flex h-8 w-8 items-center justify-center rounded-sm bg-ink text-gold transition-transform group-hover:scale-105">
              <Sparkles size={16} />
            </div>
            <span className="font-serif text-xl font-bold text-ink tracking-tight">
              Booking
            </span>
          </Link>

          {/* Desktop nav */}
          <div className="hidden md:flex items-center gap-1">
            {navLinks.map(({ href, label, auth }) => {
              if (auth && !isAuth) return null;
              return (
                <Link
                  key={href}
                  href={href}
                  className={cn(
                    "px-4 py-2 rounded-sm text-sm font-medium transition-all",
                    pathname.startsWith(href)
                      ? "bg-ink text-cream"
                      : "text-stone-600 hover:text-ink hover:bg-stone-100"
                  )}
                >
                  {label}
                </Link>
              );
            })}

            {isAdmin && (
              <Link
                href="/admin"
                className={cn(
                  "flex items-center gap-1.5 px-4 py-2 rounded-sm text-sm font-medium transition-all",
                  pathname.startsWith("/admin")
                    ? "bg-gold text-ink"
                    : "text-gold hover:bg-gold/10"
                )}
              >
                <Shield size={14} />
                Админ
              </Link>
            )}

            {isAuth ? (
              <button
                onClick={handleLogout}
                className="ml-2 flex items-center gap-1.5 px-4 py-2 rounded-sm text-sm font-medium text-stone-500 hover:text-red-600 hover:bg-red-50 transition-all"
              >
                <LogOut size={14} />
                Выйти
              </button>
            ) : (
              <div className="ml-2 flex items-center gap-2">
                <Link
                  href="/auth/login"
                  className="px-4 py-2 rounded-sm text-sm font-medium text-stone-600 hover:text-ink transition-colors"
                >
                  Войти
                </Link>
                <Link
                  href="/auth/register"
                  className="px-4 py-2 rounded-sm text-sm font-semibold bg-ink text-cream hover:bg-stone-800 transition-colors"
                >
                  Регистрация
                </Link>
              </div>
            )}
          </div>

          {/* Mobile burger */}
          <button
            className="md:hidden p-2 rounded-sm text-stone-600 hover:bg-stone-100 transition-colors"
            onClick={() => setMobileOpen(!mobileOpen)}
          >
            {mobileOpen ? <X size={20} /> : <Menu size={20} />}
          </button>
        </div>
      </div>

      {/* Mobile menu */}
      {mobileOpen && (
        <div className="md:hidden border-t border-stone-200 bg-cream animate-fade-in">
          <div className="px-4 py-3 space-y-1">
            {navLinks.map(({ href, label, icon: Icon, auth }) => {
              if (auth && !isAuth) return null;
              return (
                <Link
                  key={href}
                  href={href}
                  onClick={() => setMobileOpen(false)}
                  className={cn(
                    "flex items-center gap-3 px-3 py-2.5 rounded-sm text-sm font-medium transition-all",
                    pathname.startsWith(href)
                      ? "bg-ink text-cream"
                      : "text-stone-600 hover:bg-stone-100"
                  )}
                >
                  <Icon size={16} />
                  {label}
                </Link>
              );
            })}

            {isAdmin && (
              <Link
                href="/admin"
                onClick={() => setMobileOpen(false)}
                className="flex items-center gap-3 px-3 py-2.5 rounded-sm text-sm font-medium text-gold hover:bg-gold/10 transition-all"
              >
                <Shield size={16} />
                Панель администратора
              </Link>
            )}

            <div className="pt-2 border-t border-stone-200">
              {isAuth ? (
                <button
                  onClick={handleLogout}
                  className="flex w-full items-center gap-3 px-3 py-2.5 rounded-sm text-sm font-medium text-red-600 hover:bg-red-50 transition-all"
                >
                  <LogOut size={16} />
                  Выйти
                </button>
              ) : (
                <div className="flex flex-col gap-2">
                  <Link
                    href="/auth/login"
                    onClick={() => setMobileOpen(false)}
                    className="px-3 py-2.5 text-sm font-medium text-stone-600 hover:bg-stone-100 rounded-sm transition-colors"
                  >
                    Войти
                  </Link>
                  <Link
                    href="/auth/register"
                    onClick={() => setMobileOpen(false)}
                    className="px-3 py-2.5 text-sm font-semibold bg-ink text-cream rounded-sm text-center transition-colors"
                  >
                    Регистрация
                  </Link>
                </div>
              )}
            </div>
          </div>
        </div>
      )}
    </nav>
  );
}
