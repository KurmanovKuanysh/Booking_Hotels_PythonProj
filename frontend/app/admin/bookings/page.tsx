"use client";

import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { bookingApi } from "@/lib/services";
import { Spinner, Empty } from "@/components/ui";
import { Button } from "@/components/ui/Button";
import toast from "react-hot-toast";
import { Trash2, CalendarDays, RefreshCw } from "lucide-react";
import { formatDate, formatPrice, statusLabel, statusColor } from "@/lib/utils";
import { cn } from "@/lib/utils";
import type { BookingStatus } from "@/types";

const STATUSES: BookingStatus[] = ["pending", "confirmed", "cancelled", "completed"];

export default function AdminBookingsPage() {
  const qc = useQueryClient();

  const { data: bookings, isLoading } = useQuery({
    queryKey: ["admin-bookings"],
    queryFn: bookingApi.all,
  });

  const updateStatusMutation = useMutation({
    mutationFn: ({ id, status }: { id: number; status: string }) =>
      bookingApi.updateStatus(id, status),
    onSuccess: () => {
      toast.success("Статус обновлён");
      qc.invalidateQueries({ queryKey: ["admin-bookings"] });
    },
  });

  const deleteMutation = useMutation({
    mutationFn: bookingApi.delete,
    onSuccess: () => {
      toast.success("Бронирование удалено");
      qc.invalidateQueries({ queryKey: ["admin-bookings"] });
    },
    onError: (err: unknown) => {
      const msg =
        (err as { response?: { data?: { detail?: string } } })?.response?.data
          ?.detail ?? "Ошибка удаления";
      toast.error(msg);
    },
  });

  const updateAllMutation = useMutation({
    mutationFn: bookingApi.all,
    onSuccess: () => {
      toast.success("Статусы обновлены");
      qc.invalidateQueries({ queryKey: ["admin-bookings"] });
    },
  });

  return (
    <div>
      <div className="flex items-center justify-between mb-6">
        <h1 className="font-serif text-2xl font-bold text-ink">Бронирования</h1>
        <Button
          variant="secondary"
          size="sm"
          className="gap-1.5"
          onClick={() => updateAllMutation.mutate()}
          loading={updateAllMutation.isPending}
        >
          <RefreshCw size={14} />
          Обновить статусы
        </Button>
      </div>

      {isLoading ? (
        <div className="flex justify-center py-16">
          <Spinner />
        </div>
      ) : !bookings?.length ? (
        <Empty title="Бронирований нет" icon={<CalendarDays size={48} />} />
      ) : (
        <div className="bg-white border border-stone-200 rounded-sm overflow-hidden">
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b border-stone-100 bg-stone-50">
                <th className="text-left px-4 py-3 text-xs font-semibold uppercase tracking-wider text-stone-500">ID</th>
                <th className="text-left px-4 py-3 text-xs font-semibold uppercase tracking-wider text-stone-500">Комната / Юзер</th>
                <th className="text-left px-4 py-3 text-xs font-semibold uppercase tracking-wider text-stone-500 hidden md:table-cell">Даты</th>
                <th className="text-left px-4 py-3 text-xs font-semibold uppercase tracking-wider text-stone-500">Сумма</th>
                <th className="text-left px-4 py-3 text-xs font-semibold uppercase tracking-wider text-stone-500">Статус</th>
                <th className="text-right px-4 py-3 text-xs font-semibold uppercase tracking-wider text-stone-500">Действия</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-stone-100">
              {bookings.map((b) => (
                <tr key={b.id} className="hover:bg-stone-50 transition-colors">
                  <td className="px-4 py-3 font-mono text-stone-400">#{b.id}</td>
                  <td className="px-4 py-3">
                    <p className="text-stone-700">Комната #{b.r_id}</p>
                    <p className="text-xs text-stone-400">Юзер #{b.user_id}</p>
                  </td>
                  <td className="px-4 py-3 hidden md:table-cell text-stone-600">
                    <p className="text-xs">{formatDate(b.check_in)}</p>
                    <p className="text-xs text-stone-400">→ {formatDate(b.check_out)}</p>
                  </td>
                  <td className="px-4 py-3 font-mono font-semibold text-gold">
                    {formatPrice(b.total_price)}
                  </td>
                  <td className="px-4 py-3">
                    <select
                      className={cn(
                        "text-xs font-semibold rounded-sm border px-2 py-1 cursor-pointer focus:outline-none",
                        statusColor(b.status)
                      )}
                      value={b.status}
                      onChange={(e) =>
                        updateStatusMutation.mutate({
                          id: b.id,
                          status: e.target.value,
                        })
                      }
                    >
                      {STATUSES.map((s) => (
                        <option key={s} value={s}>
                          {statusLabel(s)}
                        </option>
                      ))}
                    </select>
                  </td>
                  <td className="px-4 py-3 text-right">
                    <Button
                      size="sm"
                      variant="danger"
                      onClick={() => {
                        if (confirm(`Удалить бронирование #${b.id}?`)) {
                          deleteMutation.mutate(b.id);
                        }
                      }}
                      disabled={
                        !["cancelled", "completed"].includes(b.status)
                      }
                    >
                      <Trash2 size={13} />
                    </Button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
