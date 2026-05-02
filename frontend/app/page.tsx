import Link from "next/link";
import { Search, Star, Shield, Clock } from "lucide-react";

export default function HomePage() {
  return (
    <div className="flex flex-col">
      {/* Hero */}
      <section className="relative overflow-hidden bg-ink text-cream">
        <div className="absolute inset-0 bg-hero-pattern opacity-60" />
        {/* Decorative */}
        <div className="absolute top-0 right-0 w-1/2 h-full opacity-5">
          <div className="absolute top-10 right-10 w-64 h-64 rounded-full border border-gold" />
          <div className="absolute top-32 right-32 w-40 h-40 rounded-full border border-gold" />
          <div className="absolute bottom-20 right-20 w-80 h-80 rounded-full border border-gold/50" />
        </div>

        <div className="relative mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-24 md:py-36">
          <div className="max-w-2xl">
            <div className="inline-flex items-center gap-2 mb-6 px-3 py-1.5 rounded-sm border border-gold/30 bg-gold/10">
              <Star size={12} className="text-gold fill-gold" />
              <span className="text-xs font-semibold text-gold tracking-widest uppercase">
                Премиум бронирование
              </span>
            </div>

            <h1 className="font-serif text-4xl md:text-6xl font-bold leading-tight mb-6">
              Найдите идеальный
              <span className="block text-gold">отель для отдыха</span>
            </h1>

            <p className="text-stone-300 text-lg mb-10 leading-relaxed max-w-lg">
              Тысячи отелей по всему миру. Удобное бронирование, честные цены,
              мгновенное подтверждение.
            </p>

            <div className="flex flex-col sm:flex-row gap-3">
              <Link
                href="/hotels"
                className="inline-flex items-center justify-center gap-2 px-8 py-4 bg-gold text-ink font-semibold rounded-sm hover:bg-gold-light transition-all active:scale-95"
              >
                <Search size={18} />
                Найти отель
              </Link>
              <Link
                href="/auth/register"
                className="inline-flex items-center justify-center gap-2 px-8 py-4 border border-stone-600 text-cream font-medium rounded-sm hover:border-stone-400 hover:bg-stone-800 transition-all"
              >
                Создать аккаунт
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* Features */}
      <section className="py-16 md:py-24 bg-cream">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {[
              {
                icon: Search,
                title: "Умный поиск",
                desc: "Фильтруйте отели по городу, звёздам и цене. Находите идеальный вариант за секунды.",
              },
              {
                icon: Clock,
                title: "Мгновенное бронирование",
                desc: "Бронируйте номера онлайн и получайте подтверждение сразу. Никаких ожиданий.",
              },
              {
                icon: Shield,
                title: "Безопасные сделки",
                desc: "Ваши данные защищены. Отмена бронирования согласно политике отеля.",
              },
            ].map(({ icon: Icon, title, desc }) => (
              <div
                key={title}
                className="flex flex-col items-start gap-4 p-6 bg-white border border-stone-200 rounded-sm"
              >
                <div className="flex h-10 w-10 items-center justify-center rounded-sm bg-ink text-gold">
                  <Icon size={20} />
                </div>
                <div>
                  <h3 className="font-serif text-lg font-semibold text-ink mb-1">
                    {title}
                  </h3>
                  <p className="text-sm text-stone-500 leading-relaxed">{desc}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA */}
      <section className="py-16 bg-stone-100 border-y border-stone-200">
        <div className="mx-auto max-w-3xl px-4 sm:px-6 lg:px-8 text-center">
          <h2 className="font-serif text-3xl md:text-4xl font-bold text-ink mb-4">
            Готовы к путешествию?
          </h2>
          <p className="text-stone-500 mb-8">
            Зарегистрируйтесь и начните бронировать отели прямо сейчас.
          </p>
          <Link
            href="/hotels"
            className="inline-flex items-center gap-2 px-8 py-4 bg-ink text-cream font-semibold rounded-sm hover:bg-stone-800 transition-all active:scale-95"
          >
            Смотреть отели
          </Link>
        </div>
      </section>
    </div>
  );
}
