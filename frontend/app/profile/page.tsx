"use client";

import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { userApi, authApi, reviewApi } from "@/lib/services";
import { useAuthStore } from "@/store/auth";
import { Spinner, Stars, Empty } from "@/components/ui";
import { Button } from "@/components/ui/Button";
import { Input } from "@/components/ui/Input";
import { formatDate } from "@/lib/utils";
import toast from "react-hot-toast";
import { useState } from "react";
import { useRouter } from "next/navigation";
import { User, Mail, Shield, Pencil, Trash2, MessageSquare, Lock } from "lucide-react";
import { cn } from "@/lib/utils";

export default function ProfilePage() {
  const { user, isAuth, setUser, logout } = useAuthStore();
  const router = useRouter();
  const qc = useQueryClient();
  const [tab, setTab] = useState<"info" | "password" | "reviews">("info");
  const [editMode, setEditMode] = useState(false);
  const [name, setName] = useState(user?.name ?? "");
  const [email, setEmail] = useState(user?.email ?? "");

  const { data: reviews, isLoading: reviewsLoading } = useQuery({
    queryKey: ["my-reviews"],
    queryFn: reviewApi.myReviews,
    enabled: isAuth && tab === "reviews",
  });

  const updateMutation = useMutation({
    mutationFn: () => userApi.updateMe({ name, email }),
    onSuccess: (updated) => {
      setUser(updated);
      toast.success("Профиль обновлён");
      setEditMode(false);
    },
    onError: () => toast.error("Ошибка обновления"),
  });

  const deleteMutation = useMutation({
    mutationFn: userApi.deleteMe,
    onSuccess: () => {
      logout();
      router.push("/");
      toast.success("Аккаунт удалён");
    },
  });

  // Password change state
  const [currPass, setCurrPass] = useState("");
  const [newPass, setNewPass] = useState("");
  const [confirmPass, setConfirmPass] = useState("");

  const passMutation = useMutation({
    mutationFn: () =>
      authApi.changePassword({
        current_password: currPass,
        new_password: newPass,
        confirm_password: confirmPass,
      }),
    onSuccess: () => {
      toast.success("Пароль изменён");
      setCurrPass("");
      setNewPass("");
      setConfirmPass("");
    },
    onError: (err: unknown) => {
      const msg =
        (err as { response?: { data?: { detail?: string } } })?.response?.data
          ?.detail ?? "Ошибка";
      toast.error(msg);
    },
  });

  const deleteReviewMutation = useMutation({
    mutationFn: reviewApi.delete,
    onSuccess: () => {
      toast.success("Отзыв удалён");
      qc.invalidateQueries({ queryKey: ["my-reviews"] });
    },
  });

  if (!isAuth) {
    return (
      <div className="mx-auto max-w-4xl px-4 py-24 text-center">
        <User size={48} className="text-stone-300 mx-auto mb-4" />
        <h2 className="font-serif text-2xl font-bold text-ink mb-2">
          Войдите в аккаунт
        </h2>
        <Button onClick={() => router.push("/auth/login")} className="mt-4">
          Войти
        </Button>
      </div>
    );
  }

  const tabs = [
    { key: "info" as const, label: "Профиль", icon: User },
    { key: "password" as const, label: "Пароль", icon: Lock },
    { key: "reviews" as const, label: "Мои отзывы", icon: MessageSquare },
  ];

  return (
    <div className="mx-auto max-w-3xl px-4 sm:px-6 lg:px-8 py-10">
      <h1 className="font-serif text-3xl font-bold text-ink mb-8">Мой профиль</h1>

      {/* Tabs */}
      <div className="flex gap-1 mb-8 border-b border-stone-200">
        {tabs.map(({ key, label, icon: Icon }) => (
          <button
            key={key}
            onClick={() => setTab(key)}
            className={cn(
              "flex items-center gap-2 px-4 py-2.5 text-sm font-medium transition-all -mb-px border-b-2",
              tab === key
                ? "border-gold text-gold"
                : "border-transparent text-stone-500 hover:text-ink"
            )}
          >
            <Icon size={15} />
            {label}
          </button>
        ))}
      </div>

      {/* Tab: Info */}
      {tab === "info" && (
        <div className="bg-white border border-stone-200 rounded-sm p-6 space-y-5">
          {editMode ? (
            <>
              <Input
                label="Имя"
                value={name}
                onChange={(e) => setName(e.target.value)}
                icon={<User size={16} />}
              />
              <Input
                label="Email"
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                icon={<Mail size={16} />}
              />
              <div className="flex gap-3">
                <Button
                  loading={updateMutation.isPending}
                  onClick={() => updateMutation.mutate()}
                >
                  Сохранить
                </Button>
                <Button variant="ghost" onClick={() => setEditMode(false)}>
                  Отмена
                </Button>
              </div>
            </>
          ) : (
            <>
              <div className="flex items-center gap-3 pb-4 border-b border-stone-100">
                <div className="flex h-14 w-14 items-center justify-center rounded-sm bg-ink text-gold font-serif text-xl font-bold">
                  {user?.name?.[0]?.toUpperCase() ?? "?"}
                </div>
                <div>
                  <p className="font-semibold text-ink text-lg">{user?.name}</p>
                  <p className="text-stone-500 text-sm">{user?.email}</p>
                </div>
              </div>

              <div className="grid grid-cols-2 gap-4 text-sm">
                <div>
                  <p className="text-xs text-stone-400 mb-0.5">Роль</p>
                  <div className="flex items-center gap-1.5">
                    <Shield size={13} className="text-gold" />
                    <span className="font-medium">{user?.role}</span>
                  </div>
                </div>
                <div>
                  <p className="text-xs text-stone-400 mb-0.5">Статус</p>
                  <span
                    className={cn(
                      "inline-flex items-center px-2 py-0.5 rounded-sm text-xs font-semibold border",
                      user?.is_active
                        ? "bg-emerald-50 text-emerald-700 border-emerald-200"
                        : "bg-red-50 text-red-600 border-red-200"
                    )}
                  >
                    {user?.is_active ? "Активен" : "Неактивен"}
                  </span>
                </div>
              </div>

              <div className="flex gap-3 pt-2">
                <Button
                  variant="secondary"
                  size="sm"
                  onClick={() => {
                    setName(user?.name ?? "");
                    setEmail(user?.email ?? "");
                    setEditMode(true);
                  }}
                  className="gap-1"
                >
                  <Pencil size={14} />
                  Редактировать
                </Button>
                <Button
                  variant="danger"
                  size="sm"
                  loading={deleteMutation.isPending}
                  onClick={() => {
                    if (confirm("Удалить аккаунт? Это действие необратимо.")) {
                      deleteMutation.mutate();
                    }
                  }}
                  className="gap-1"
                >
                  <Trash2 size={14} />
                  Удалить аккаунт
                </Button>
              </div>
            </>
          )}
        </div>
      )}

      {/* Tab: Password */}
      {tab === "password" && (
        <div className="bg-white border border-stone-200 rounded-sm p-6 space-y-5">
          <Input
            label="Текущий пароль"
            type="password"
            value={currPass}
            onChange={(e) => setCurrPass(e.target.value)}
            icon={<Lock size={16} />}
          />
          <Input
            label="Новый пароль"
            type="password"
            value={newPass}
            onChange={(e) => setNewPass(e.target.value)}
            icon={<Lock size={16} />}
          />
          <Input
            label="Подтвердите пароль"
            type="password"
            value={confirmPass}
            onChange={(e) => setConfirmPass(e.target.value)}
            icon={<Lock size={16} />}
          />
          <Button
            loading={passMutation.isPending}
            onClick={() => passMutation.mutate()}
            disabled={!currPass || !newPass || !confirmPass}
          >
            Изменить пароль
          </Button>
        </div>
      )}

      {/* Tab: Reviews */}
      {tab === "reviews" && (
        <div>
          {reviewsLoading ? (
            <div className="flex justify-center py-12">
              <Spinner />
            </div>
          ) : !reviews?.length ? (
            <Empty
              title="Отзывов пока нет"
              description="Оставьте отзыв после завершённого бронирования"
              icon={<MessageSquare size={48} />}
            />
          ) : (
            <div className="space-y-4">
              {reviews.map((review) => (
                <div
                  key={review.id}
                  className="bg-white border border-stone-200 rounded-sm p-5"
                >
                  <div className="flex items-start justify-between mb-2">
                    <div className="flex items-center gap-2">
                      <Stars count={review.rating} size={14} />
                      <span className="text-xs text-stone-400">
                        {formatDate(review.created_at)}
                      </span>
                    </div>
                    <button
                      onClick={() => deleteReviewMutation.mutate(review.id)}
                      className="text-stone-400 hover:text-red-500 transition-colors"
                    >
                      <Trash2 size={14} />
                    </button>
                  </div>
                  <p className="text-sm text-stone-700">{review.comment}</p>
                  <p className="text-xs text-stone-400 mt-2">
                    Отель #{review.hotel_id} · Бронирование #{review.booking_id}
                  </p>
                </div>
              ))}
            </div>
          )}
        </div>
      )}
    </div>
  );
}
