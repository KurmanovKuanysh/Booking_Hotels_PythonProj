"use client";

import { useState } from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { hotelApi, roomApi } from "@/lib/services";
import { Spinner, Empty } from "@/components/ui";
import { Button } from "@/components/ui/Button";
import { Input } from "@/components/ui/Input";
import toast from "react-hot-toast";
import { Plus, Trash2, BedDouble, X } from "lucide-react";
import { formatPrice } from "@/lib/utils";
import type { RoomCreate } from "@/types";

const emptyForm: RoomCreate = {
  room_number: "",
  r_t_id: 1,
  capacity: 2,
  price_per_day: 0,
  floor: 1,
  description: "",
};

export default function AdminRoomsPage() {
  const qc = useQueryClient();
  const [selectedHotelId, setSelectedHotelId] = useState<number | null>(null);
  const [showCreate, setShowCreate] = useState(false);
  const [form, setForm] = useState<RoomCreate>(emptyForm);

  const { data: hotels, isLoading: hotelsLoading } = useQuery({
    queryKey: ["admin-hotels"],
    queryFn: () => hotelApi.list({ page: 1, size: 100 }),
  });

  const { data: rooms, isLoading: roomsLoading } = useQuery({
    queryKey: ["admin-rooms", selectedHotelId],
    queryFn: () => roomApi.byHotel(selectedHotelId!),
    enabled: !!selectedHotelId,
  });

  const createMutation = useMutation({
    mutationFn: () => roomApi.create(selectedHotelId!, form),
    onSuccess: () => {
      toast.success("Комната добавлена");
      qc.invalidateQueries({ queryKey: ["admin-rooms", selectedHotelId] });
      setShowCreate(false);
      setForm(emptyForm);
    },
    onError: (err: unknown) => {
      const msg =
        (err as { response?: { data?: { detail?: string } } })?.response?.data
          ?.detail ?? "Ошибка";
      toast.error(msg);
    },
  });

  const deleteMutation = useMutation({
    mutationFn: roomApi.delete,
    onSuccess: () => {
      toast.success("Комната удалена");
      qc.invalidateQueries({ queryKey: ["admin-rooms", selectedHotelId] });
    },
  });

  const selectedHotel = hotels?.find((h) => h.id === selectedHotelId);

  return (
    <div>
      <div className="flex items-center justify-between mb-6">
        <h1 className="font-serif text-2xl font-bold text-ink">Комнаты</h1>
      </div>

      {/* Hotel selector */}
      <div className="bg-white border border-stone-200 rounded-sm p-4 mb-6">
        <label className="text-xs font-semibold uppercase tracking-wider text-stone-500 block mb-1.5">
          Выберите отель
        </label>
        {hotelsLoading ? (
          <Spinner className="h-5 w-5" />
        ) : (
          <select
            className="w-full rounded-sm border border-stone-300 bg-white px-4 py-2.5 text-sm text-ink focus:border-gold focus:outline-none"
            value={selectedHotelId ?? ""}
            onChange={(e) => {
              setSelectedHotelId(Number(e.target.value) || null);
              setShowCreate(false);
            }}
          >
            <option value="">— выберите отель —</option>
            {hotels?.map((h) => (
              <option key={h.id} value={h.id}>
                {h.name} ({h.city})
              </option>
            ))}
          </select>
        )}
      </div>

      {!selectedHotelId ? null : (
        <>
          <div className="flex items-center justify-between mb-4">
            <h2 className="font-semibold text-ink">
              {selectedHotel?.name} — комнаты
              <span className="ml-2 text-sm text-stone-400 font-normal">
                ({rooms?.length ?? 0})
              </span>
            </h2>
            <Button
              size="sm"
              onClick={() => setShowCreate(!showCreate)}
              className="gap-1.5"
            >
              {showCreate ? <X size={14} /> : <Plus size={14} />}
              {showCreate ? "Отмена" : "Добавить комнату"}
            </Button>
          </div>

          {/* Create form */}
          {showCreate && (
            <div className="bg-white border border-stone-200 rounded-sm p-5 mb-5 animate-fade-in">
              <h3 className="font-semibold text-ink mb-4">Новая комната</h3>
              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 mb-4">
                <Input
                  label="Номер комнаты"
                  placeholder="101"
                  value={form.room_number}
                  onChange={(e) =>
                    setForm((f) => ({ ...f, room_number: e.target.value }))
                  }
                />
                <Input
                  label="Вместимость (гостей)"
                  type="number"
                  min={1}
                  value={form.capacity}
                  onChange={(e) =>
                    setForm((f) => ({ ...f, capacity: Number(e.target.value) }))
                  }
                />
                <Input
                  label="Цена за ночь (₸)"
                  type="number"
                  min={0}
                  value={form.price_per_day}
                  onChange={(e) =>
                    setForm((f) => ({
                      ...f,
                      price_per_day: Number(e.target.value),
                    }))
                  }
                />
                <Input
                  label="Этаж"
                  type="number"
                  min={1}
                  value={form.floor}
                  onChange={(e) =>
                    setForm((f) => ({ ...f, floor: Number(e.target.value) }))
                  }
                />
                <Input
                  label="ID типа комнаты"
                  type="number"
                  min={1}
                  value={form.r_t_id}
                  onChange={(e) =>
                    setForm((f) => ({ ...f, r_t_id: Number(e.target.value) }))
                  }
                />
                <Input
                  label="Описание"
                  placeholder="Опционально..."
                  value={form.description ?? ""}
                  onChange={(e) =>
                    setForm((f) => ({ ...f, description: e.target.value }))
                  }
                />
              </div>
              <Button
                loading={createMutation.isPending}
                onClick={() => createMutation.mutate()}
                disabled={!form.room_number || !form.price_per_day}
              >
                Создать
              </Button>
            </div>
          )}

          {/* Rooms list */}
          {roomsLoading ? (
            <div className="flex justify-center py-12">
              <Spinner />
            </div>
          ) : !rooms?.length ? (
            <Empty
              title="Комнат нет"
              description="Добавьте первую комнату"
              icon={<BedDouble size={48} />}
            />
          ) : (
            <div className="bg-white border border-stone-200 rounded-sm overflow-hidden">
              <table className="w-full text-sm">
                <thead>
                  <tr className="border-b border-stone-100 bg-stone-50">
                    <th className="text-left px-4 py-3 text-xs font-semibold uppercase tracking-wider text-stone-500">
                      №
                    </th>
                    <th className="text-left px-4 py-3 text-xs font-semibold uppercase tracking-wider text-stone-500">
                      Этаж
                    </th>
                    <th className="text-left px-4 py-3 text-xs font-semibold uppercase tracking-wider text-stone-500">
                      Гостей
                    </th>
                    <th className="text-left px-4 py-3 text-xs font-semibold uppercase tracking-wider text-stone-500">
                      Цена / ночь
                    </th>
                    <th className="text-left px-4 py-3 text-xs font-semibold uppercase tracking-wider text-stone-500 hidden md:table-cell">
                      Описание
                    </th>
                    <th className="text-right px-4 py-3 text-xs font-semibold uppercase tracking-wider text-stone-500">
                      Действия
                    </th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-stone-100">
                  {rooms.map((room) => (
                    <tr
                      key={room.id}
                      className="hover:bg-stone-50 transition-colors"
                    >
                      <td className="px-4 py-3 font-semibold text-ink">
                        {room.room_number}
                      </td>
                      <td className="px-4 py-3 text-stone-600">{room.floor}</td>
                      <td className="px-4 py-3 text-stone-600">
                        {room.capacity}
                      </td>
                      <td className="px-4 py-3 font-mono font-semibold text-gold">
                        {formatPrice(room.price_per_day)}
                      </td>
                      <td className="px-4 py-3 text-stone-400 text-xs hidden md:table-cell max-w-xs truncate">
                        {room.description ?? "—"}
                      </td>
                      <td className="px-4 py-3 text-right">
                        <Button
                          size="sm"
                          variant="danger"
                          onClick={() => {
                            if (confirm(`Удалить комнату ${room.room_number}?`)) {
                              deleteMutation.mutate(room.id);
                            }
                          }}
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
        </>
      )}
    </div>
  );
}