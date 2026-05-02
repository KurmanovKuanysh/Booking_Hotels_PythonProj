import Link from "next/link";
import { Sparkles } from "lucide-react";

export function Footer() {
  return (
    <footer className="border-t border-stone-200 bg-cream mt-auto">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-10">
        <div className="flex flex-col md:flex-row items-center justify-between gap-6">
          <Link href="/" className="flex items-center gap-2">
            <div className="flex h-7 w-7 items-center justify-center rounded-sm bg-ink text-gold">
              <Sparkles size={14} />
            </div>
            <span className="font-serif text-lg font-bold text-ink">Booking</span>
          </Link>

          <nav className="flex items-center gap-6">
            <Link href="/hotels" className="text-sm text-stone-500 hover:text-ink transition-colors">
              Отели
            </Link>
            <Link href="/bookings" className="text-sm text-stone-500 hover:text-ink transition-colors">
              Бронирования
            </Link>
            <Link href="/profile" className="text-sm text-stone-500 hover:text-ink transition-colors">
              Профиль
            </Link>
          </nav>

          <p className="text-xs text-stone-400">
            © {new Date().getFullYear()} Booking. Все права защищены.
          </p>
        </div>
      </div>
    </footer>
  );
}
