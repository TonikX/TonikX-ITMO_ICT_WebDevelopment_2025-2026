export type RoomType = 'single' | 'double' | 'triple';

export interface Room {
  id: number;
  number: number;
  floor: number;
  room_type: RoomType;
  capacity: number;
  daily_rate: string;
  phone_number: string;
  is_active: boolean;
  occupied_places: number;
}

export interface Client {
  id: number;
  passport_number: string;
  last_name: string;
  first_name: string;
  middle_name?: string;
  city: string;
  phone?: string;
  email?: string;
  notes?: string;
  full_name: string;
}

export interface Stay {
  id: number;
  client: number;
  room: number;
  check_in: string;
  check_out?: string | null;
  status: 'active' | 'completed';
  total_cost: string;
}

export interface RoomStay {
  id: number;
  client: {
    id: number;
    full_name: string;
    city: string;
  };
  check_in: string;
  check_out?: string | null;
  status: 'active' | 'completed';
  total_cost: string;
}

export interface Employee {
  id: number;
  last_name: string;
  first_name: string;
  middle_name?: string;
  status: 'active' | 'fired';
  hire_date: string;
  termination_date?: string | null;
  assignments: CleaningAssignment[];
}

export interface CleaningAssignment {
  id?: number;
  floor: number;
  weekday: string;
}

export interface FreeRoomsSummary {
  total_free_rooms: number;
  by_type: { room_type: RoomType; label: string; count: number }[];
}

export interface QuarterlyReport {
  period: {
    quarter: number;
    year: number;
    start: string;
    end: string;
  };
  clients_per_room: { room__id: number; room__number: number; client_count: number }[];
  rooms_per_floor: { floor: number; room_count: number }[];
  income_per_room: { room__id: number; room__number: number; total_income: string }[];
  total_income: number;
}

