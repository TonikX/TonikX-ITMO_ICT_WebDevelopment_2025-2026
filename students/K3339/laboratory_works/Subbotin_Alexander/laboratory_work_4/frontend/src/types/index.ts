// User types
export interface User {
  id: number;
  username: string;
  email: string;
  is_active: boolean;
  is_admin: boolean;
  created_at: string;
}

export interface UserProfile {
  id: number;
  user_id: number;
  date_of_birth: string | null;
}

export interface UserCreate {
  username: string;
  email: string;
  password: string;
}

export interface UserLogin {
  username: string;
  password: string;
}

export interface Token {
  access_token: string;
  token_type: string;
}

// Tour types
export interface Tour {
  id: number;
  title: string;
  agency: string;
  description: string | null;
  start_date: string;
  end_date: string;
  price: number;
  city: string;
  payment_terms: string | null;
}

export interface TourCreate {
  title: string;
  agency: string;
  description?: string;
  start_date: string;
  end_date: string;
  price: number;
  city: string;
  payment_terms?: string;
}

export interface TourUpdate {
  title?: string;
  agency?: string;
  description?: string;
  start_date?: string;
  end_date?: string;
  price?: number;
  city?: string;
  payment_terms?: string;
}

// Reservation types
export type ReservationStatus = 'pending' | 'confirmed' | 'rejected';

export interface Reservation {
  id: number;
  tour_id: number;
  user_id: number;
  notes: string | null;
  status: ReservationStatus;
  created_at: string;
  tour: Tour;
}

export interface ReservationCreate {
  tour_id: number;
  notes?: string;
}

export interface ReservationUpdate {
  notes?: string;
  status?: ReservationStatus;
}

// Admin reservation type with username
export interface ReservationAdmin extends Reservation {
  username: string | null;
}

// Admin stats type
export interface AdminStats {
  confirmed_reservations: number;
  total_revenue: number;
  total_customers: number;
}

// Review types
export interface Review {
  id: number;
  tour_id: number;
  user_id: number | null;
  text: string;
  rating: number;
  created_at: string;
  updated_at: string | null;
  username?: string;
}

export interface ReviewCreate {
  tour_id: number;
  text: string;
  rating: number;
}

export interface ReviewUpdate {
  text?: string;
  rating?: number;
}

// API Response types
export interface ApiError {
  detail: string;
}
