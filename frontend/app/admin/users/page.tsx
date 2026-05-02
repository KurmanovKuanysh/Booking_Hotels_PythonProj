"use client";

import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { adminUserApi } from "@/lib/services";
import { Spinner, Badge, Empty } from "@/components/ui";
import { Button } from "@/components/ui/Button";
import { Input } from "@/components/ui/Input";
import toast from "react-hot-toast";
import { Trash2, Search, Users, ShieldCheck } from "lucide-react";
import { useState } from "react";
import { cn } from "@/lib/utils";
import type { User } from "@/types";

export default function AdminUsersPage() {
  const qc = useQueryClient();
  const [search, setSearch] = useState("");

  const { data: users, isLoading } = useQuery({
    queryKey: ["admin-users"],
    queryFn: adminUserApi.all,
  });

  const deleteMutation = useMutation({
    mutationFn: (id: number) => adminUserApi.deleteWithBookings(id),
    onSuccess: () => {
      toast.success("Пользователь удалён");
      qc.invalidateQueries({ queryKey: ["admin-users"] });
    },
    onError: () => toast.error("Ошибка удаления"),
  });

  const toggleActiveMutation = useMutation({
    mutationFn: ({ id, user }: { id: number; user: User }) =>
      adminUserApi.edit(id, { is_active: !user.is_active, role: user.role }),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["admin-users"] });
    },
  });

  const filtered = users?.filter(
    (u) =>
      u.name.toLowerCase().includes(search.toLowerCase()) ||
      u.email.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <div>
      <div className="flex items-center justify-between mb-6">
        <h1 className="font-serif text-2xl font-bold text-ink">Пользователи</h1>
        <span className="text-sm text-stone-400">{users?.length ?? 0} всего</span>
      </div>

      <div className="mb-4">
        <Input
          placeholder="Поиск по имени или email..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          icon={<Search size={16} />}
        />
      </div>

      {isLoading ? (
        <div className="flex justify-center py-16">
          <Spinner />
        </div>
      ) : !filtered?.length ? (
        <Empty
          title="Пользователи не найдены"
          icon={<Users size={48} />}
        />
      ) : (
        <div className="bg-white border border-stone-200 rounded-sm overflow-hidden">
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b border-stone-100 bg-stone-50">
                <th className="text-left px-4 py-3 text-xs font-semibold uppercase tracking-wider text-stone-500">ID</th>
                <th className="text-left px-4 py-3 text-xs font-semibold uppercase tracking-wider text-stone-500">Пользователь</th>
                <th className="text-left px-4 py-3 text-xs font-semibold uppercase tracking-wider text-stone-500 hidden md:table-cell">Роль</th>
                <th className="text-left px-4 py-3 text-xs font-semibold uppercase tracking-wider text-stone-500">Статус</th>
                <th className="text-right px-4 py-3 text-xs font-semibold uppercase tracking-wider text-stone-500">Действия</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-stone-100">
              {filtered.map((user) => (
                <tr key={user.id} className="hover:bg-stone-50 transition-colors">
                  <td className="px-4 py-3 font-mono text-stone-400">#{user.id}</td>
                  <td className="px-4 py-3">
                    <div>
                      <p className="font-medium text-ink">{user.name}</p>
                      <p className="text-xs text-stone-400">{user.email}</p>
                    </div>
                  </td>
                  <td className="px-4 py-3 hidden md:table-cell">
                    <span className={cn(
                      "inline-flex items-center gap-1 px-2 py-0.5 rounded-sm text-xs font-semibold border",
                      user.role === "S-ADMIN" ? "bg-gold/15 text-gold-dark border-gold/30" :
                      user.role === "ADMIN" ? "bg-blue-50 text-blue-700 border-blue-200" :
                      "bg-stone-100 text-stone-600 border-stone-200"
                    )}>
                      {user.role === "ADMIN" || user.role === "S-ADMIN" ? <ShieldCheck size={11} /> : null}
                      {user.role}
                    </span>
                  </td>
                  <td className="px-4 py-3">
                    <button
                      onClick={() => toggleActiveMutation.mutate({ id: user.id, user })}
                      className={cn(
                        "inline-flex items-center px-2 py-0.5 rounded-sm text-xs font-semibold border transition-opacity hover:opacity-70",
                        user.is_active
                          ? "bg-emerald-50 text-emerald-700 border-emerald-200"
                          : "bg-red-50 text-red-600 border-red-200"
                      )}
                    >
                      {user.is_active ? "Активен" : "Неактивен"}
                    </button>
                  </td>
                  <td className="px-4 py-3 text-right">
                    <Button
                      variant="danger"
                      size="sm"
                      onClick={() => {
                        if (confirm(`Удалить ${user.name}?`)) {
                          deleteMutation.mutate(user.id);
                        }
                      }}
                      loading={deleteMutation.isPending}
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
