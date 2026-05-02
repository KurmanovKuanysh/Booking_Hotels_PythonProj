"use client";

import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";
import Link from "next/link";
import { useRouter } from "next/navigation";
import toast from "react-hot-toast";
import { Mail, Lock } from "lucide-react";
import { authApi, userApi } from "@/lib/services";
import { useAuthStore } from "@/store/auth";
import { Button } from "@/components/ui/Button";
import { Input } from "@/components/ui/Input";

const schema = z.object({
  email: z.string().email("Некорректный email"),
  password: z.string().min(8, "Минимум 8 символов"),
});

type FormData = z.infer<typeof schema>;

export default function LoginPage() {
  const router = useRouter();
  const setAuth = useAuthStore((s) => s.setAuth);

  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm<FormData>({ resolver: zodResolver(schema) });

  const onSubmit = async (data: FormData) => {
    try {
      const tokens = await authApi.login({
        username: data.email,
        password: data.password,
      });

      // Temporarily set token to fetch user
      localStorage.setItem("access_token", tokens.access_token);
      if (tokens.refresh_token) {
        localStorage.setItem("refresh_token", tokens.refresh_token);
      }

      const user = await userApi.me();
      setAuth(user, tokens.access_token, tokens.refresh_token ?? "");

      toast.success(`Добро пожаловать, ${user.name}!`);
      router.push("/hotels");
    } catch (err: unknown) {
      const msg =
        (err as { response?: { data?: { detail?: string } } })?.response?.data
          ?.detail ?? "Неверный email или пароль";
      toast.error(msg);
    }
  };

  return (
    <div className="min-h-[calc(100vh-4rem)] flex items-center justify-center px-4 py-12">
      <div className="w-full max-w-md">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="font-serif text-3xl font-bold text-ink mb-2">
            Войдите в аккаунт
          </h1>
          <p className="text-stone-500 text-sm">
            Нет аккаунта?{" "}
            <Link
              href="/auth/register"
              className="text-gold hover:text-gold-dark font-medium transition-colors"
            >
              Зарегистрируйтесь
            </Link>
          </p>
        </div>

        <div className="bg-white border border-stone-200 rounded-sm p-8 shadow-sm">
          <form onSubmit={handleSubmit(onSubmit)} className="space-y-5">
            <Input
              id="email"
              label="Email"
              type="email"
              placeholder="you@example.com"
              icon={<Mail size={16} />}
              error={errors.email?.message}
              {...register("email")}
            />

            <Input
              id="password"
              label="Пароль"
              type="password"
              placeholder="••••••••"
              icon={<Lock size={16} />}
              error={errors.password?.message}
              {...register("password")}
            />

            <Button
              type="submit"
              size="lg"
              className="w-full mt-2"
              loading={isSubmitting}
            >
              Войти
            </Button>
          </form>
        </div>
      </div>
    </div>
  );
}
