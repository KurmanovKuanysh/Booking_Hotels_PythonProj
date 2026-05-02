"use client";

import { useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { hotelApi } from "@/lib/services";
import { HotelCard } from "@/components/hotel/HotelCard";
import { Spinner, Empty } from "@/components/ui";
import { Button } from "@/components/ui/Button";
import { Input } from "@/components/ui/Input";
import { Search, SlidersHorizontal, X } from "lucide-react";
import type { HotelFilters } from "@/types";

export default function HotelsPage() {
  const [search, setSearch] = useState("");
  const [showFilters, setShowFilters] = useState(false);
  const [filters, setFilters] = useState<HotelFilters>({});
  const [page, setPage] = useState(1);
  const size = 12;

  const { data: searchResults, isFetching: searching } = useQuery({
    queryKey: ["hotels-search", search],
    queryFn: () => hotelApi.searchByName(search),
    enabled: search.length > 1,
  });

  const { data: filteredHotels, isFetching: filtering } = useQuery({
    queryKey: ["hotels-filter", filters],
    queryFn: () => hotelApi.filter(filters),
    enabled:
      !search &&
      (!!filters.city || !!filters.stars_from || !!filters.stars_to),
  });

  const { data: allHotels, isFetching: loading } = useQuery({
    queryKey: ["hotels", page],
    queryFn: () => hotelApi.list({ page, size }),
    enabled: !search && !filteredHotels,
  });

  const hotels = search
    ? searchResults
    : filters.city || filters.stars_from || filters.stars_to
    ? filteredHotels
    : allHotels;

  const isLoading = loading || searching || filtering;

  const clearFilters = () => {
    setFilters({});
    setSearch("");
  };

  const hasFilters = search || filters.city || filters.stars_from || filters.stars_to;

  return (
    <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-10">
      {/* Header */}
      <div className="mb-8">
        <h1 className="font-serif text-3xl font-bold text-ink mb-1">Отели</h1>
        <p className="text-stone-500 text-sm">Найдите идеальное место для проживания</p>
      </div>

      {/* Search + filters */}
      <div className="mb-6 flex flex-col sm:flex-row gap-3">
        <div className="flex-1">
          <Input
            placeholder="Поиск по названию отеля..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            icon={<Search size={16} />}
          />
        </div>
        <Button
          variant="secondary"
          onClick={() => setShowFilters(!showFilters)}
          className="gap-2"
        >
          <SlidersHorizontal size={16} />
          Фильтры
          {hasFilters && (
            <span className="flex h-5 w-5 items-center justify-center rounded-full bg-gold text-ink text-xs font-bold">
              !
            </span>
          )}
        </Button>
        {hasFilters && (
          <Button variant="ghost" onClick={clearFilters}>
            <X size={16} />
            Сбросить
          </Button>
        )}
      </div>

      {/* Filter panel */}
      {showFilters && (
        <div className="mb-6 p-5 bg-white border border-stone-200 rounded-sm animate-fade-in">
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
            <Input
              label="Город"
              placeholder="Алматы, Астана..."
              value={filters.city ?? ""}
              onChange={(e) =>
                setFilters((f) => ({ ...f, city: e.target.value || undefined }))
              }
            />
            <div>
              <label className="text-xs font-semibold uppercase tracking-wider text-stone-500 block mb-1.5">
                Звёзды от
              </label>
              <select
                className="w-full rounded-sm border border-stone-300 bg-white px-4 py-2.5 text-sm text-ink focus:border-gold focus:outline-none"
                value={filters.stars_from ?? 1}
                onChange={(e) =>
                  setFilters((f) => ({
                    ...f,
                    stars_from: Number(e.target.value),
                  }))
                }
              >
                {[1, 2, 3, 4, 5].map((s) => (
                  <option key={s} value={s}>{s}★</option>
                ))}
              </select>
            </div>
            <div>
              <label className="text-xs font-semibold uppercase tracking-wider text-stone-500 block mb-1.5">
                Звёзды до
              </label>
              <select
                className="w-full rounded-sm border border-stone-300 bg-white px-4 py-2.5 text-sm text-ink focus:border-gold focus:outline-none"
                value={filters.stars_to ?? 5}
                onChange={(e) =>
                  setFilters((f) => ({
                    ...f,
                    stars_to: Number(e.target.value),
                  }))
                }
              >
                {[1, 2, 3, 4, 5].map((s) => (
                  <option key={s} value={s}>{s}★</option>
                ))}
              </select>
            </div>
          </div>
        </div>
      )}

      {/* Results */}
      {isLoading ? (
        <div className="flex items-center justify-center py-24">
          <Spinner />
        </div>
      ) : !hotels?.length ? (
        <Empty
          title="Отели не найдены"
          description="Попробуйте изменить параметры поиска"
          icon={<Search size={48} />}
        />
      ) : (
        <>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-5">
            {hotels.map((hotel) => (
              <HotelCard key={hotel.id} hotel={hotel} />
            ))}
          </div>

          {/* Pagination (only for all hotels view) */}
          {!search && !filteredHotels && (
            <div className="mt-10 flex items-center justify-center gap-3">
              <Button
                variant="secondary"
                size="sm"
                disabled={page === 1}
                onClick={() => setPage((p) => p - 1)}
              >
                Назад
              </Button>
              <span className="text-sm text-stone-500 font-mono">
                стр. {page}
              </span>
              <Button
                variant="secondary"
                size="sm"
                disabled={(hotels?.length ?? 0) < size}
                onClick={() => setPage((p) => p + 1)}
              >
                Вперёд
              </Button>
            </div>
          )}
        </>
      )}
    </div>
  );
}
