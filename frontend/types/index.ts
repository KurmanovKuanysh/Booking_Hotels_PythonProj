// Auth
export interface TokenPair {
  access_token: string;
  refresh_token: string | null;
  token_type: string;
}

export interface LoginRequest {
  username: string;
  password: string;
}

export interface RegisterRequest {
  name: string;
  email: string;
  password: string;
}

// User
export type UserRole = "S-ADMIN" | "ADMIN" | "USER";

export interface User {
  id: number;
  name: string;
  email: string;
  role: UserRole;
  is_active: boolean;
}

export interface UserEdit {
  name?: string;
  email?: string;
  password?: string;
}

export interface UserChangePassword {
  current_password: string;
  new_password: string;
  confirm_password: string;
}

// Hotel
export interface Hotel {
  id: number;
  name: string;
  city: string;
  address: string;
  stars: number;
  rating_sum: number;
  rating_count: number;
}

export interface HotelCreate {
  name: string;
  city: string;
  address: string;
  stars: number;
  description?: string;
}

export interface HotelEdit {
  name?: string;
  city?: string;
  address?: string;
  stars?: number;
  description?: string;
}

// Room
export interface Room {
  id: number;
  room_number: string;
  r_t_id: number;
  capacity: number;
  price_per_day: number;
  floor: number;
  description: string | null;
}

export interface RoomCreate {
  room_number: string;
  r_t_id: number;
  capacity: number;
  price_per_day: number;
  floor: number;
  description?: string;
}

// Booking
export type BookingStatus = "pending" | "confirmed" | "cancelled" | "completed";

export interface Booking {
  id: number;
  r_id: number;
  check_in: string;
  check_out: string;
  status: BookingStatus;
  user_id: number;
  total_price: number;
}

export interface BookingCreate {
  r_id: number;
  check_in: string;
  check_out: string;
  guest_count?: number;
}

export interface BookingEdit {
  r_id?: number;
  check_in?: string;
  check_out?: string;
}

export interface BookingCancelResponse {
  message: string;
  penalty: number;
  refund: number;
}

// Review
export interface Review {
  id: number;
  booking_id: number;
  user_id: number;
  hotel_id: number;
  rating: number;
  comment: string;
  created_at: string;
}

export interface ReviewCreate {
  booking_id: number;
  rating: number;
  comment: string;
}

export interface ReviewEdit {
  rating?: number;
  comment?: string;
}

// Filters
export interface HotelFilters {
  stars_from?: number;
  stars_to?: number;
  city?: string;
}

export interface RoomFilters {
  capacity?: number;
  min_price?: number;
  max_price?: number;
  room_type?: string;
}

// Pagination
export interface PaginationParams {
  page?: number;
  size?: number;
}
