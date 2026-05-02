"use client";

import { useState } from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { bookingApi, reviewApi } from "@/lib/services";
import { useAuthStore } from "@/store/auth";
import { Spinner, Empty, Badge, Stars } from "@/components/ui";
import { Button } from "@/components/ui/Button";
import { Input } from "@/components/ui/Input";
import { formatDate, formatPrice, statusLabel, statusColor } from "@/lib/utils";
import toast from "react-hot-toast";
import { CalendarDays, X, MessageSquare, ChevronDown, ChevronUp } from "lucide-react";
import { cn } from "@/lib/utils";
import type { Booking } from "@/types";
import { useRouter } from "next/navigation";

export default function BookingsPage() {
  const { isAuth } = useAuthStore();
  const router = useRouter();
  const qc = useQueryClient();

  const { data: bookings, isLoading } = useQuery({
    queryKey: ["bookings-me"],
    queryFn: bookingApi.myBookings,
    enabled: isAuth,
  });

  if (!isAuth) {
    return (
      <div className="mx-auto max-w-4xl px-4 py-24 text-center">
        <CalendarDays size={48} className="text-stone-300 mx-auto mb-4" />
        <h2 className="font-serif text-2xl font-bold text-ink mb-2">
          Войдите, чтобы увидеть бронирования
        </h2>
        <Button onClick={() => router.push("/auth/login")} className="mt-4">
          Войти
        </Button>
      </div>
    );
  }

  if (isLoading)
    return (
      <div className="flex items-center justify-center py-32">
        <Spinner />
      </div>
    );

  return (
    <div className="mx-auto max-w-4xl px-4 sm:px-6 lg:px-8 py-10">
      <div className="mb-8">
        <h1 className="font-serif text-3xl font-bold text-ink mb-1">
          Мои бронирования
        </h1>
        <p className="text-stone-500 text-sm">
          {bookings?.length ?? 0} бронирований
        </p>
      </div>

      {!bookings?.length ? (
        <Empty
          title="Бронирований пока нет"
          description="Найдите и забронируйте отель"
          icon={<CalendarDays size={48} />}
          action={
            <Button onClick={() => router.push("/hotels")}>
              Найти отель
            </Button>
          }
        />
      ) : (
        <div className="space-y-4">
          {bookings.map((booking) => (
            <BookingCard
              key={booking.id}
              booking={booking}
              onCancelled={() =>
                qc.invalidateQueries({ queryKey: ["bookings-me"] })
              }
            />
          ))}
        </div>
      )}
    </div>
  );
}

function BookingCard({
  booking,
  onCancelled,
}: {
  booking: Booking;
  onCancelled: () => void;
}) {
  const qc = useQueryClient();
  const [showReview, setShowReview] = useState(false);
  const [rating, setRating] = useState(5);
  const [comment, setComment] = useState("");

  const cancelMutation = useMutation({
    mutationFn: () => bookingApi.cancel(booking.id),
    onSuccess: (data) => {
      toast.success(
        `Отменено. Штраф: ${formatPrice(data.penalty)}, возврат: ${formatPrice(data.refund)}`
      );
      onCancelled();
    },
    onError: () => toast.error("Не удалось отменить"),
  });

  const reviewMutation = useMutation({
    mutationFn: () =>
      reviewApi.addReview(0, {
        booking_id: booking.id,
        rating,
        comment,
      }),
    onSuccess: () => {
      toast.success("Отзыв добавлен!");
      setShowReview(false);
      qc.invalidateQueries({ queryKey: ["my-reviews"] });
    },
    onError: (err: unknown) => {
      const msg =
        (err as { response?: { data?: { detail?: string } } })?.response?.data
          ?.detail ?? "Ошибка";
      toast.error(msg);
    },
  });

  const canCancel = ["pending", "confirmed"].includes(booking.status);
  const canReview = booking.status === "completed";

  return (
    <div className="bg-white border border-stone-200 rounded-sm overflow-hidden">
      <div className="p-5">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 mb-4">
          <div>
            <div className="flex items-center gap-2 mb-1">
              <span className="font-mono text-xs text-stone-400">
                #{booking.id}
              </span>
              <span
                className={cn(
                  "inline-flex items-center px-2.5 py-0.5 rounded-sm text-xs font-semibold border",
                  statusColor(booking.status)
                )}
              >
                {statusLabel(booking.status)}
              </span>
            </div>
            <p className="font-semibold text-ink">Комната #{booking.r_id}</p>
          </div>
          <div className="text-right">
            <p className="font-mono font-bold text-gold text-lg">
              {formatPrice(booking.total_price)}
            </p>
          </div>
        </div>

        <div className="grid grid-cols-2 gap-4 text-sm text-stone-600 mb-4">
          <div>
            <p className="text-xs text-stone-400 mb-0.5">Заезд</p>
            <p className="font-medium">{formatDate(booking.check_in)}</p>
          </div>
          <div>
            <p className="text-xs text-stone-400 mb-0.5">Выезд</p>
            <p className="font-medium">{formatDate(booking.check_out)}</p>
          </div>
        </div>

        <div className="flex items-center gap-2 flex-wrap">
          {canCancel && (
            <Button
              variant="danger"
              size="sm"
              loading={cancelMutation.isPending}
              onClick={() => cancelMutation.mutate()}
              className="gap-1"
            >
              <X size={14} />
              Отменить
            </Button>
          )}
          {canReview && (
            <Button
              variant="secondary"
              size="sm"
              onClick={() => setShowReview(!showReview)}
              className="gap-1"
            >
              <MessageSquare size={14} />
              {showReview ? "Скрыть" : "Написать отзыв"}
            </Button>
          )}
        </div>
      </div>

      {/* Review form */}
      {showReview && (
        <div className="border-t border-stone-100 p-5 bg-stone-50 animate-fade-in">
          <h4 className="font-semibold text-sm text-ink mb-3">Ваш отзыв</h4>
          <div className="space-y-3">
            <div>
              <label className="text-xs font-semibold uppercase tracking-wider text-stone-500 block mb-1.5">
                Оценка
              </label>
              <div className="flex items-center gap-1">
                {[1, 2, 3, 4, 5].map((s) => (
                  <button
                    key={s}
                    onClick={() => setRating(s)}
                    className="transition-transform hover:scale-110"
                  >
                    <svg
                      width={24}
                      height={24}
                      viewBox="0 0 24 24"
                      fill={s <= rating ? "#C9A84C" : "none"}
                      stroke={s <= rating ? "#C9A84C" : "#D1C9BC"}
                      strokeWidth={2}
                    >
                      <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2" />
                    </svg>
                  </button>
                ))}
              </div>
            </div>
            <Input
              label="Комментарий"
              placeholder="Поделитесь впечатлениями..."
              value={comment}
              onChange={(e) => setComment(e.target.value)}
            />
            <Button
              size="sm"
              loading={reviewMutation.isPending}
              onClick={() => reviewMutation.mutate()}
              disabled={!comment.trim()}
            >
              Отправить отзыв
            </Button>
          </div>
        </div>
      )}
    </div>
  );
}
