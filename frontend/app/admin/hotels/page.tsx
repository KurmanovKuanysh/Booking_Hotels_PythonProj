"use client";

import { useState } from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { hotelApi, roomApi } from "@/lib/services";
import { Spinner, Empty, Stars } from "@/components/ui";
import { Button } from "@/components/ui/Button";
import { Input } from "@/components/ui/Input";
import toast from "react-hot-toast";
import { Plus, Trash2, Pencil, Hotel, X, Check } from "lucide-react";
import type { HotelCreate, HotelEdit } from "@/types";

export default function AdminHotelsPage() {
  const qc = useQueryClient();
  const [showCreate, setShowCreate] = useState(false);
  const [editId, setEditId] = useState<number | null>(null);

  // Create form state
  const [form, setForm] = useState<HotelCreate>({
    name: "",
    city: "",
    address: "",
    stars: 3,
    description: "",
  });

  // Edit form state
  const [editForm, setEditForm] = useState<HotelEdit>({});

  const { data: hotels, isLoading } = useQuery({
    queryKey: ["admin-hotels"],
    queryFn: () => hotelApi.list({ page: 1, size: 100 }),
  });

  const createMutation = useMutation({
    mutationFn: () => hotelApi.create(form),
    onSuccess: () => {
      toast.success("Отель создан");
      qc.invalidateQueries({ queryKey: ["admin-hotels"] });
      setShowCreate(false);
      setForm({ name: "", city: "", address: "", stars: 3 });
    },
    onError: () => toast.error("Ошибка создания"),
  });

  const updateMutation = useMutation({
    mutationFn: ({ id, data }: { id: number; data: HotelEdit }) =>
      hotelApi.update(id, data),
    onSuccess: () => {
      toast.success("Отель обновлён");
      qc.invalidateQueries({ queryKey: ["admin-hotels"] });
      setEditId(null);
    },
  });

  const deleteMutation = useMutation({
    mutationFn: hotelApi.delete,
    onSuccess: () => {
      toast.success("Отель удалён");
      qc.invalidateQueries({ queryKey: ["admin-hotels"] });
    },
  });

  return (
    <div>
      <div className="flex items-center justify-between mb-6">
        <h1 className="font-serif text-2xl font-bold text-ink">Отели</h1>
        <Button
          size="sm"
          onClick={() => setShowCreate(!showCreate)}
          className="gap-1.5"
        >
          {showCreate ? <X size={14} /> : <Plus size={14} />}
          {showCreate ? "Отмена" : "Добавить отель"}
        </Button>
      </div>

      {/* Create form */}
      {showCreate && (
        <div className="bg-white border border-stone-200 rounded-sm p-5 mb-6 animate-fade-in">
          <h3 className="font-semibold text-ink mb-4">Новый отель</h3>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 mb-4">
            <Input
              label="Название"
              value={form.name}
              onChange={(e) => setForm((f) => ({ ...f, name: e.target.value }))}
            />
            <Input
              label="Город"
              value={form.city}
              onChange={(e) => setForm((f) => ({ ...f, city: e.target.value }))}
            />
            <Input
              label="Адрес"
              value={form.address}
              onChange={(e) => setForm((f) => ({ ...f, address: e.target.value }))}
            />
            <div>
              <label className="text-xs font-semibold uppercase tracking-wider text-stone-500 block mb-1.5">
                Звёзды
              </label>
              <select
                className="w-full rounded-sm border border-stone-300 bg-white px-4 py-2.5 text-sm focus:border-gold focus:outline-none"
                value={form.stars}
                onChange={(e) =>
                  setForm((f) => ({ ...f, stars: Number(e.target.value) }))
                }
              >
                {[1, 2, 3, 4, 5].map((s) => (
                  <option key={s} value={s}>{s}★</option>
                ))}
              </select>
            </div>
            <div className="sm:col-span-2">
              <Input
                label="Описание"
                value={form.description ?? ""}
                onChange={(e) =>
                  setForm((f) => ({ ...f, description: e.target.value }))
                }
              />
            </div>
          </div>
          <Button
            loading={createMutation.isPending}
            onClick={() => createMutation.mutate()}
            disabled={!form.name || !form.city || !form.address}
          >
            Создать
          </Button>
        </div>
      )}

      {isLoading ? (
        <div className="flex justify-center py-16">
          <Spinner />
        </div>
      ) : !hotels?.length ? (
        <Empty title="Отелей нет" icon={<Hotel size={48} />} />
      ) : (
        <div className="bg-white border border-stone-200 rounded-sm overflow-hidden">
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b border-stone-100 bg-stone-50">
                <th className="text-left px-4 py-3 text-xs font-semibold uppercase tracking-wider text-stone-500">ID</th>
                <th className="text-left px-4 py-3 text-xs font-semibold uppercase tracking-wider text-stone-500">Отель</th>
                <th className="text-left px-4 py-3 text-xs font-semibold uppercase tracking-wider text-stone-500 hidden lg:table-cell">Город</th>
                <th className="text-left px-4 py-3 text-xs font-semibold uppercase tracking-wider text-stone-500">Звёзды</th>
                <th className="text-right px-4 py-3 text-xs font-semibold uppercase tracking-wider text-stone-500">Действия</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-stone-100">
              {hotels.map((hotel) => (
                <tr key={hotel.id} className="hover:bg-stone-50 transition-colors">
                  <td className="px-4 py-3 font-mono text-stone-400">#{hotel.id}</td>
                  <td className="px-4 py-3">
                    {editId === hotel.id ? (
                      <input
                        className="border border-gold rounded-sm px-2 py-1 text-sm w-full focus:outline-none"
                        defaultValue={hotel.name}
                        onChange={(e) =>
                          setEditForm((f) => ({ ...f, name: e.target.value }))
                        }
                      />
                    ) : (
                      <span className="font-medium">{hotel.name}</span>
                    )}
                  </td>
                  <td className="px-4 py-3 text-stone-600 hidden lg:table-cell">{hotel.city}</td>
                  <td className="px-4 py-3">
                    <Stars count={hotel.stars} size={12} />
                  </td>
                  <td className="px-4 py-3 text-right">
                    <div className="flex items-center justify-end gap-2">
                      {editId === hotel.id ? (
                        <>
                          <Button
                            size="sm"
                            variant="gold"
                            onClick={() =>
                              updateMutation.mutate({
                                id: hotel.id,
                                data: editForm,
                              })
                            }
                            loading={updateMutation.isPending}
                          >
                            <Check size={13} />
                          </Button>
                          <Button
                            size="sm"
                            variant="ghost"
                            onClick={() => setEditId(null)}
                          >
                            <X size={13} />
                          </Button>
                        </>
                      ) : (
                        <>
                          <Button
                            size="sm"
                            variant="secondary"
                            onClick={() => {
                              setEditId(hotel.id);
                              setEditForm({ name: hotel.name });
                            }}
                          >
                            <Pencil size={13} />
                          </Button>
                          <Button
                            size="sm"
                            variant="danger"
                            onClick={() => {
                              if (confirm(`Удалить ${hotel.name}?`)) {
                                deleteMutation.mutate(hotel.id);
                              }
                            }}
                          >
                            <Trash2 size={13} />
                          </Button>
                        </>
                      )}
                    </div>
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
