import Link from "next/link";
import type { Hotel } from "@/types";
import { getHotelRating } from "@/lib/utils";
import { MapPin, Star } from "lucide-react";
import { Stars } from "@/components/ui";

interface HotelCardProps {
  hotel: Hotel;
}

export function HotelCard({ hotel }: HotelCardProps) {
  const rating = getHotelRating(hotel.rating_sum, hotel.rating_count);

  return (
    <Link href={`/hotels/${hotel.id}`} className="block group">
      <div className="bg-white border border-stone-200 rounded-sm overflow-hidden transition-all group-hover:shadow-md group-hover:-translate-y-0.5">
        {/* Placeholder image */}
        <div className="h-44 bg-gradient-to-br from-stone-100 to-stone-200 relative overflow-hidden">
          <div className="absolute inset-0 flex items-center justify-center opacity-20">
            <svg width="80" height="80" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1">
              <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/>
              <polyline points="9 22 9 12 15 12 15 22"/>
            </svg>
          </div>
          <div className="absolute top-3 right-3 flex items-center gap-1 bg-white/90 backdrop-blur-sm px-2 py-1 rounded-sm shadow-sm">
            <Star size={11} className="text-gold fill-gold" />
            <span className="text-xs font-semibold text-ink">{rating}</span>
          </div>
        </div>

        <div className="p-4">
          <div className="flex items-start justify-between gap-2 mb-2">
            <h3 className="font-serif font-semibold text-ink text-base leading-snug group-hover:text-gold transition-colors line-clamp-1">
              {hotel.name}
            </h3>
            <Stars count={hotel.stars} size={12} />
          </div>

          <div className="flex items-center gap-1 text-stone-500">
            <MapPin size={12} className="shrink-0" />
            <span className="text-xs truncate">{hotel.city}, {hotel.address}</span>
          </div>

          {hotel.rating_count > 0 && (
            <div className="mt-3 pt-3 border-t border-stone-100 flex items-center justify-between">
              <span className="text-xs text-stone-400">{hotel.rating_count} отзывов</span>
              <div className="flex items-center gap-1">
                <span className="text-base font-bold text-ink font-mono">{rating}</span>
                <span className="text-xs text-stone-400">/ 5</span>
              </div>
            </div>
          )}
        </div>
      </div>
    </Link>
  );
}
