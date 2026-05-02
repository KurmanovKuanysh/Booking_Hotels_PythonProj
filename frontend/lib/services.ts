import api from "./api";
import type {
  TokenPair,
  LoginRequest,
  RegisterRequest,
  User,
  UserEdit,
  UserChangePassword,
  Hotel,
  HotelCreate,
  HotelEdit,
  HotelFilters,
  Room,
  RoomCreate,
  Booking,
  BookingCreate,
  BookingEdit,
  BookingCancelResponse,
  Review,
  ReviewCreate,
  ReviewEdit,
  PaginationParams,
} from "@/types";

// ── Auth ──────────────────────────────────────────────────────────────────────
export const authApi = {
  register: (data: RegisterRequest) =>
    api.post<User>("/auth/register", data).then((r) => r.data),

  login: (data: LoginRequest) => {
    const form = new URLSearchParams();
    form.append("username", data.username);
    form.append("password", data.password);
    return api
      .post<TokenPair>("/auth/login", form, {
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
      })
      .then((r) => r.data);
  },

  logout: (refresh_token: string) =>
    api.post("/auth/logout", { refresh_token }),

  changePassword: (data: UserChangePassword) =>
    api.patch("/auth/change-password", data),
};

// ── Users ─────────────────────────────────────────────────────────────────────
export const userApi = {
  me: () => api.get<User>("/users/me").then((r) => r.data),

  updateMe: (data: UserEdit) =>
    api.patch<User>("/users/me", data).then((r) => r.data),

  deleteMe: () => api.delete("/users/me"),
};

// ── Hotels ────────────────────────────────────────────────────────────────────
export const hotelApi = {
  list: (params?: PaginationParams) =>
    api.get<Hotel[]>("/hotels", { params }).then((r) => r.data),

  popular: (limit = 6) =>
    api.get<Hotel[]>("/hotels/popular", { params: { limit } }).then((r) => r.data),

  searchByName: (name: string) =>
    api.get<Hotel[]>("/hotels/search/name", { params: { name } }).then((r) => r.data),

  searchByAddress: (address: string) =>
    api.get<Hotel[]>("/hotels/search/address", { params: { address } }).then((r) => r.data),

  filter: (filters: HotelFilters) =>
    api.get<Hotel[]>("/hotels/search/filter", { params: filters }).then((r) => r.data),

  // Admin
  create: (data: HotelCreate) =>
    api.post<Hotel>("/admin/hotels", data).then((r) => r.data),

  update: (id: number, data: HotelEdit) =>
    api.patch<Hotel>(`/admin/hotels/${id}/edit`, data).then((r) => r.data),

  delete: (id: number) => api.delete(`/admin/hotels/${id}`),

  getById: (id: number) =>
    api.get<Hotel>(`/admin/hotels/${id}`).then((r) => r.data),
};

// ── Rooms ─────────────────────────────────────────────────────────────────────
export const roomApi = {
  byHotel: (hotelId: number) =>
    api.get<Room[]>(`/hotels/${hotelId}/rooms`).then((r) => r.data),

  available: (
    hotelId: number,
    check_in: string,
    check_out: string
  ) =>
    api
      .get<Room[]>(`/hotels/${hotelId}/rooms/available`, {
        params: { check_in, check_out },
      })
      .then((r) => r.data),

  allAvailable: (params: {
    city?: string;
    check_in?: string;
    check_out?: string;
    guests?: number;
  }) =>
    api.get<Room[]>("/rooms/available", { params }).then((r) => r.data),

  myBooked: () =>
    api.get<Room[]>("/rooms/my-booked-rooms").then((r) => r.data),

  checkAvailability: (
    roomId: number,
    check_in: string,
    check_out: string
  ) =>
    api
      .get<boolean>(`/rooms/${roomId}/check-availability`, {
        params: { check_in, check_out },
      })
      .then((r) => r.data),

  // Admin
  create: (hotelId: number, data: RoomCreate) =>
    api.post<Room>(`/admin/hotels/${hotelId}/rooms`, data).then((r) => r.data),

  delete: (roomId: number) => api.delete(`/admin/rooms/${roomId}`),
};

// ── Bookings ──────────────────────────────────────────────────────────────────
export const bookingApi = {
  create: (data: BookingCreate) =>
    api.post<Booking>("/bookings", data).then((r) => r.data),

  myBookings: () =>
    api.get<Booking[]>("/bookings/me").then((r) => r.data),

  edit: (id: number, data: BookingEdit) =>
    api.patch<Booking>(`/bookings/${id}`, data).then((r) => r.data),

  cancel: (id: number) =>
    api.patch<BookingCancelResponse>(`/bookings/${id}/cancel`).then((r) => r.data),

  // Admin
  all: () => api.get<Booking[]>("/admin/bookings").then((r) => r.data),

  getById: (id: number) =>
    api.get<Booking>(`/admin/bookings/${id}`).then((r) => r.data),

  delete: (id: number) =>
    api.delete<boolean>(`/admin/bookings/${id}`).then((r) => r.data),

  updateStatus: (id: number, status: string) =>
    api
      .patch<boolean>(`/admin/bookings/${id}/status`, null, {
        params: { status },
      })
      .then((r) => r.data),
};

// ── Reviews ───────────────────────────────────────────────────────────────────
export const reviewApi = {
  myReviews: () =>
    api.get<Review[]>("/users/reviews").then((r) => r.data),

  addReview: (hotelId: number, data: ReviewCreate) =>
    api.post<Review>(`/hotels/${hotelId}/reviews`, data).then((r) => r.data),

  edit: (reviewId: number, data: ReviewEdit) =>
    api.patch<Review>(`/reviews/${reviewId}`, data).then((r) => r.data),

  delete: (reviewId: number) => api.delete(`/reviews/${reviewId}`),
};

// ── Admin Users ───────────────────────────────────────────────────────────────
export const adminUserApi = {
  all: () => api.get<User[]>("/admin/users").then((r) => r.data),

  getById: (id: number) =>
    api.get<User>(`/admin/users/${id}`).then((r) => r.data),

  delete: (id: number) => api.delete(`/admin/users/${id}`),

  deleteWithBookings: (id: number) =>
    api.delete(`/admin/users/${id}/delete-cascade`),

  edit: (id: number, data: Partial<User> & { is_active?: boolean }) =>
    api.patch<User>(`/admin/users/${id}/edit/force`, data).then((r) => r.data),
};
