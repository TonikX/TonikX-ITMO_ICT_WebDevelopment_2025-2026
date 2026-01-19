import api from './client';
import type { Reservation, ReservationCreate, ReservationUpdate, ReservationAdmin, AdminStats, ReservationStatus } from '@/types';

export const reservationsApi = {
  // Получение бронирований текущего пользователя
  getMy: async (params?: { limit?: number; offset?: number }): Promise<Reservation[]> => {
    const response = await api.get<Reservation[]>('/reservations/my', { params });
    return response.data;
  },

  // Получение бронирования по ID
  getById: async (id: number): Promise<Reservation> => {
    const response = await api.get<Reservation>(`/reservations/${id}`);
    return response.data;
  },

  // Создание бронирования
  create: async (data: ReservationCreate): Promise<Reservation> => {
    const response = await api.post<Reservation>('/reservations/', data);
    return response.data;
  },

  // Обновление бронирования
  update: async (id: number, data: ReservationUpdate): Promise<Reservation> => {
    const response = await api.put<Reservation>(`/reservations/${id}`, data);
    return response.data;
  },

  // Удаление бронирования
  delete: async (id: number): Promise<void> => {
    await api.delete(`/reservations/${id}`);
  },

  // [ADMIN] Получение всех бронирований
  getAllAdmin: async (params?: { limit?: number; offset?: number; status?: ReservationStatus }): Promise<ReservationAdmin[]> => {
    const response = await api.get<ReservationAdmin[]>('/reservations/admin/all', { params });
    return response.data;
  },

  // [ADMIN] Подтверждение бронирования
  confirm: async (id: number): Promise<Reservation> => {
    const response = await api.put<Reservation>(`/reservations/admin/${id}/confirm`);
    return response.data;
  },

  // [ADMIN] Отклонение бронирования
  reject: async (id: number): Promise<Reservation> => {
    const response = await api.put<Reservation>(`/reservations/admin/${id}/reject`);
    return response.data;
  },

  // [ADMIN] Получение статистики
  getStats: async (): Promise<AdminStats> => {
    const response = await api.get<AdminStats>('/reservations/admin/stats');
    return response.data;
  },
};

export default reservationsApi;
