"use client";

import { useState } from "react";
import { useParams, useRouter } from "next/navigation";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { hotelApi, roomApi, reviewApi, bookingApi } from "@/lib/services";
import { useAuthStore } from "@/store/auth";
import { Spinner, Stars, Badge, Empty } from "@/components/ui";
import { Button } from "@/components/ui/Button";
import { Input } from "@/components/ui/Input";
import { formatDate, formatPrice, calcNights, statusLabel, statusColor } from "@/lib/utils";
import toast from "react-hot-toast";
import {
  MapPin, Star, Users, BedDouble, Building2, ArrowLeft,
  CalendarDays, MessageSquare, ChevronDown, ChevronUp
} from "lucide-react";
import type { Room, Review } from "@/types";

export default function HotelDetailPage() {
  const params = useParams();
  const router = useRouter();
  const hotelId = Number(params.id);
  const { user, isAuth } = useAuthStore();
  const qc = useQueryClient();

  const [checkIn, setCheckIn] = useState("");
  const [checkOut, setCheckOut] = useState("");
  const [guests, setGuests] = useState(1);
  const [bookingRoomId, setBookingRoomId] = useState<number | null>(null);
  const [showReviews, setShowReviews] = useState(false);

  const { data: hotel, isLoading } = useQuery({
    queryKey: ["hotel", hotelId],
    queryFn: () => hotelApi.getById(hotelId),
  });

  const { data: rooms, isFetching: loadingRooms } = useQuery({
    queryKey: ["rooms-available", hotelId, checkIn, checkOut],
    queryFn: () =>
      checkIn && checkOut
        ? roomApi.available(hotelId, checkIn, checkOut)
        : roomApi.byHotel(hotelId),
  });

  const { data: reviews } = useQuery({
    queryKey: ["hotel-reviews", hotelId],
    queryFn: async () => {
      // We get them via user's reviews filtered by hotel_id
      // The API doesn't have a public hotel reviews endpoint, so use admin or filter
      return [] as Review[];
    },
    enabled: showReviews,
  });

  const bookMutation = useMutation({
    mutationFn: () =>
      bookingApi.create({
        r_id: bookingRoomId!,
        check_in: checkIn,
        check_out: checkOut,
        guest_count: guests,
      }),
    onSuccess: () => {
      toast.success("Бронирование создано!");
      qc.invalidateQueries({ queryKey: ["bookings"] });
      router.push("/bookings");
    },
    onError: (err: unknown) => {
      const msg =
        (err as { response?: { data?: { detail?: string } } })?.response?.data?.detail ??
        "Ошибка бронирования";
      toast.error(msg);
    },
  });

  const handleBook = (roomId: number) => {
    if (!isAuth) {
      router.push("/auth/login");
      return;
    }
    if (!checkIn || !checkOut) {
      toast.error("Выберите даты заезда и выезда");
      return;
    }
    setBookingRoomId(roomId);
    bookMutation.mutate();
  };

  if (isLoading)
    return (
      <div className="flex items-center justify-center py-32">
        <Spinner />
      </div>
    );

  if (!hotel)
    return (
      <div className="flex items-center justify-center py-32">
        <p className="text-stone-500">Отель не найден</p>
      </div>
    );

  const avgRating =
    hotel.rating_count > 0
      ? (hotel.rating_sum / hotel.rating_count).toFixed(1)
      : null;

  return (
    <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-10">
      {/* Back */}
      <button
        onClick={() => router.back()}
        className="flex items-center gap-2 text-sm text-stone-500 hover:text-ink mb-6 transition-colors"
      >
        <ArrowLeft size={16} />
        Назад к отелям
      </button>

      {/* Hotel header */}
      <div className="bg-white border border-stone-200 rounded-sm overflow-hidden mb-8">
        <div className="h-48 bg-gradient-to-br from-stone-200 to-stone-100 relative">
          <div className="absolute inset-0 flex items-center justify-center opacity-10">
            <Building2 size={120} />
          </div>
          {avgRating && (
            <div className="absolute top-4 right-4 flex items-center gap-1.5 bg-white px-3 py-1.5 rounded-sm shadow">
              <Star size={14} className="text-gold fill-gold" />
              <span className="font-bold text-ink text-sm">{avgRating}</span>
              <span className="text-stone-400 text-xs">/ 5</span>
            </div>
          )}
        </div>

        <div className="p-6">
          <div className="flex flex-col sm:flex-row sm:items-start justify-between gap-4">
            <div>
              <h1 className="font-serif text-2xl md:text-3xl font-bold text-ink mb-2">
                {hotel.name}
              </h1>
              <div className="flex items-center gap-2 text-stone-500 mb-3">
                <MapPin size={14} />
                <span className="text-sm">
                  {hotel.city}, {hotel.address}
                </span>
              </div>
              <Stars count={hotel.stars} size={16} />
            </div>
            <div className="flex flex-col items-end gap-1">
              {hotel.rating_count > 0 && (
                <>
                  <span className="font-mono text-3xl font-bold text-gold">
                    {avgRating}
                  </span>
                  <span className="text-xs text-stone-400">
                    {hotel.rating_count} отзывов
                  </span>
                </>
              )}
            </div>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Rooms */}
        <div className="lg:col-span-2">
          <h2 className="font-serif text-xl font-bold text-ink mb-4 flex items-center gap-2">
            <BedDouble size={20} />
            Номера
          </h2>

          {/* Date filter */}
          <div className="bg-white border border-stone-200 rounded-sm p-4 mb-5">
            <p className="text-xs font-semibold uppercase tracking-wider text-stone-500 mb-3">
              Проверить доступность
            </p>
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
              <Input
                label="Заезд"
                type="datetime-local"
                value={checkIn}
                onChange={(e) => setCheckIn(e.target.value)}
              />
              <Input
                label="Выезд"
                type="datetime-local"
                value={checkOut}
                onChange={(e) => setCheckOut(e.target.value)}
              />
              <Input
                label="Гостей"
                type="number"
                min={1}
                value={guests}
                onChange={(e) => setGuests(Number(e.target.value))}
              />
            </div>
          </div>

          {loadingRooms ? (
            <div className="flex justify-center py-12">
              <Spinner />
            </div>
          ) : !rooms?.length ? (
            <Empty
              title="Нет доступных номеров"
              description="Попробуйте изменить даты"
              icon={<BedDouble size={48} />}
            />
          ) : (
            <div className="space-y-3">
              {rooms.map((room) => (
                <RoomRow
                  key={room.id}
                  room={room}
                  checkIn={checkIn}
                  checkOut={checkOut}
                  onBook={() => handleBook(room.id)}
                  isBooking={
                    bookMutation.isPending && bookingRoomId === room.id
                  }
                />
              ))}
            </div>
          )}
        </div>

        {/* Sidebar */}
        <div className="space-y-5">
          <div className="bg-white border border-stone-200 rounded-sm p-5">
            <h3 className="font-serif font-semibold text-ink mb-3 flex items-center gap-2">
              <MessageSquare size={16} />
              Отзывы
            </h3>
            <button
              onClick={() => setShowReviews(!showReviews)}
              className="flex items-center gap-2 text-sm text-stone-500 hover:text-ink transition-colors"
            >
              {showReviews ? (
                <>
                  Скрыть <ChevronUp size={14} />
                </>
              ) : (
                <>
                  Показать отзывы <ChevronDown size={14} />
                </>
              )}
            </button>
            {showReviews && (
              <div className="mt-4">
                {!reviews?.length ? (
                  <p className="text-sm text-stone-400">Отзывов пока нет</p>
                ) : (
                  reviews.map((r) => <ReviewItem key={r.id} review={r} />)
                )}
              </div>
            )}
          </div>

          {!isAuth && (
            <div className="bg-ink text-cream rounded-sm p-5">
              <p className="text-sm mb-3 text-stone-300">
                Войдите, чтобы бронировать номера и оставлять отзывы
              </p>
              <Button
                variant="gold"
                size="sm"
                className="w-full"
                onClick={() => router.push("/auth/login")}
              >
                Войти
              </Button>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

function RoomRow({
  room,
  checkIn,
  checkOut,
  onBook,
  isBooking,
}: {
  room: Room;
  checkIn: string;
  checkOut: string;
  onBook: () => void;
  isBooking: boolean;
}) {
  const nights = checkIn && checkOut ? calcNights(checkIn, checkOut) : null;

  return (
    <div className="bg-white border border-stone-200 rounded-sm p-4 hover:border-stone-300 transition-colors">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
        <div className="flex-1">
          <div className="flex items-center gap-2 mb-1">
            <span className="font-semibold text-ink text-sm">
              Номер {room.room_number}
            </span>
            <Badge variant="stone">Этаж {room.floor}</Badge>
          </div>
          <div className="flex items-center gap-4 text-xs text-stone-500">
            <span className="flex items-center gap-1">
              <Users size={12} />
              {room.capacity} гостей
            </span>
            <span className="font-mono text-gold font-semibold">
              {formatPrice(room.price_per_day)} / ночь
            </span>
            {nights && (
              <span className="text-stone-400">
                Итого: {formatPrice(room.price_per_day * nights)}
              </span>
            )}
          </div>
          {room.description && (
            <p className="text-xs text-stone-400 mt-1 line-clamp-1">
              {room.description}
            </p>
          )}
        </div>
        <Button
          size="sm"
          variant="gold"
          onClick={onBook}
          loading={isBooking}
          className="shrink-0"
        >
          Забронировать
        </Button>
      </div>
    </div>
  );
}

function ReviewItem({ review }: { review: Review }) {
  return (
    <div className="border-t border-stone-100 pt-3 mt-3">
      <div className="flex items-center gap-2 mb-1">
        <Stars count={review.rating} size={12} />
        <span className="text-xs text-stone-400">{formatDate(review.created_at)}</span>
      </div>
      <p className="text-sm text-stone-600">{review.comment}</p>
    </div>
  );
}
