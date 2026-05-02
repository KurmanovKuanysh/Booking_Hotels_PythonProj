"use client";

import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";
import Link from "next/link";
import { useRouter } from "next/navigation";
import toast from "react-hot-toast";
import { User, Mail, Lock } from "lucide-react";
import { authApi } from "@/lib/services";
import { Button } from "@/components/ui/Button";
import { Input } from "@/components/ui/Input";

const schema = z.object({
  name: z.string().min(3, "Минимум 3 символа"),
  email: z.string().email("Некорректный email"),
  password: z.string().min(8, "Минимум 8 символов"),
});

type FormData = z.infer<typeof schema>;

export default function RegisterPage() {
  const router = useRouter();

  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm<FormData>({ resolver: zodResolver(schema) });

  const onSubmit = async (data: FormData) => {
    try {
      await authApi.register(data);
      toast.success("Аккаунт создан! Войдите в систему.");
      router.push("/auth/login");
    } catch (err: unknown) {
      const msg =
        (err as { response?: { data?: { detail?: string } } })?.response?.data
          ?.detail ?? "Ошибка регистрации";
      toast.error(msg);
    }
  };

  return (
    <div className="min-h-[calc(100vh-4rem)] flex items-center justify-center px-4 py-12">
      <div className="w-full max-w-md">
        <div className="text-center mb-8">
          <h1 className="font-serif text-3xl font-bold text-ink mb-2">
            Создайте аккаунт
          </h1>
          <p className="text-stone-500 text-sm">
            Уже есть аккаунт?{" "}
            <Link
              href="/auth/login"
              className="text-gold hover:text-gold-dark font-medium transition-colors"
            >
              Войдите
            </Link>
          </p>
        </div>

        <div className="bg-white border border-stone-200 rounded-sm p-8 shadow-sm">
          <form onSubmit={handleSubmit(onSubmit)} className="space-y-5">
            <Input
              id="name"
              label="Имя"
              placeholder="Иван Иванов"
              icon={<User size={16} />}
              error={errors.name?.message}
              {...register("name")}
            />

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
              placeholder="Минимум 8 символов"
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
              Зарегистрироваться
            </Button>
          </form>
        </div>
      </div>
    </div>
  );
}
