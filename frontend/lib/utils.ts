import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]): string {
  return twMerge(clsx(inputs));
}

export function formatDate(date: string): string {
  return new Date(date).toLocaleDateString("ru-RU", {
    day: "numeric",
    month: "long",
    year: "numeric",
  });
}

export function formatPrice(price: number): string {
  return new Intl.NumberFormat("ru-RU", {
    style: "currency",
    currency: "KZT",
    maximumFractionDigits: 0,
  }).format(price);
}

export function calcNights(checkIn: string, checkOut: string): number {
  const diff = new Date(checkOut).getTime() - new Date(checkIn).getTime();
  return Math.max(1, Math.ceil(diff / (1000 * 60 * 60 * 24)));
}

export function getHotelRating(sum: number, count: number): string {
  if (count === 0) return "—";
  return (sum / count).toFixed(1);
}

export function statusColor(status: string): string {
  const map: Record<string, string> = {
    pending: "text-amber-600 bg-amber-50 border-amber-200",
    confirmed: "text-emerald-700 bg-emerald-50 border-emerald-200",
    cancelled: "text-red-600 bg-red-50 border-red-200",
    completed: "text-stone-600 bg-stone-100 border-stone-200",
  };
  return map[status] ?? "text-stone-500 bg-stone-50";
}

export function statusLabel(status: string): string {
  const map: Record<string, string> = {
    pending: "Ожидает",
    confirmed: "Подтверждено",
    cancelled: "Отменено",
    completed: "Завершено",
  };
  return map[status] ?? status;
}
