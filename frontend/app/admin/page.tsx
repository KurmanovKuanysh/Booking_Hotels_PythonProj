"use client";

import { useQuery } from "@tanstack/react-query";
import { adminUserApi, bookingApi, hotelApi } from "@/lib/services";
import { Spinner } from "@/components/ui";
import { Users, Hotel, CalendarDays, TrendingUp } from "lucide-react";
import Link from "next/link";

export default function AdminDashboard() {
  const { data: users } = useQuery({
    queryKey: ["admin-users"],
    queryFn: adminUserApi.all,
  });

  const { data: bookings } = useQuery({
    queryKey: ["admin-bookings"],
    queryFn: bookingApi.all,
  });

  const { data: hotels } = useQuery({
    queryKey: ["admin-hotels"],
    queryFn: () => hotelApi.list({ page: 1, size: 100 }),
  });

  const stats = [
    {
      label: "Пользователи",
      value: users?.length ?? "—",
      icon: Users,
      href: "/admin/users",
      color: "bg-blue-50 text-blue-600",
    },
    {
      label: "Отели",
      value: hotels?.length ?? "—",
      icon: Hotel,
      href: "/admin/hotels",
      color: "bg-emerald-50 text-emerald-600",
    },
    {
      label: "Бронирования",
      value: bookings?.length ?? "—",
      icon: CalendarDays,
      href: "/admin/bookings",
      color: "bg-amber-50 text-amber-600",
    },
    {
      label: "Выручка (всего)",
      value: bookings
        ? `${bookings.reduce((s, b) => s + b.total_price, 0).toLocaleString()} ₸`
        : "—",
      icon: TrendingUp,
      href: "/admin/bookings",
      color: "bg-gold/10 text-gold-dark",
    },
  ];

  return (
    <div>
      <h1 className="font-serif text-2xl font-bold text-ink mb-8">Дашборд</h1>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5 mb-10">
        {stats.map(({ label, value, icon: Icon, href, color }) => (
          <Link key={label} href={href}>
            <div className="bg-white border border-stone-200 rounded-sm p-5 hover:shadow-sm hover:-translate-y-0.5 transition-all">
              <div className="flex items-start justify-between mb-3">
                <p className="text-xs font-semibold uppercase tracking-wider text-stone-500">
                  {label}
                </p>
                <div className={`flex h-8 w-8 items-center justify-center rounded-sm ${color}`}>
                  <Icon size={16} />
                </div>
              </div>
              <p className="font-mono text-2xl font-bold text-ink">{value}</p>
            </div>
          </Link>
        ))}
      </div>

      {/* Recent bookings */}
      <div className="bg-white border border-stone-200 rounded-sm">
        <div className="px-5 py-4 border-b border-stone-100">
          <h2 className="font-semibold text-ink">Последние бронирования</h2>
        </div>
        <div className="divide-y divide-stone-100">
          {bookings?.slice(0, 10).map((b) => (
            <div key={b.id} className="px-5 py-3 flex items-center justify-between text-sm">
              <div className="flex items-center gap-4">
                <span className="font-mono text-stone-400">#{b.id}</span>
                <span className="text-stone-600">
                  Комната #{b.r_id} · Пользователь #{b.user_id}
                </span>
              </div>
              <div className="flex items-center gap-3">
                <span className="font-mono font-semibold text-gold">
                  {b.total_price.toLocaleString()} ₸
                </span>
                <span className="text-xs px-2 py-0.5 rounded-sm border bg-stone-50 text-stone-600 border-stone-200">
                  {b.status}
                </span>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
