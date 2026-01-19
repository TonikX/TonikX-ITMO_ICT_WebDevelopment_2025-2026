import api from './client';
import type { Tour, TourCreate, TourUpdate } from '@/types';

export const toursApi = {
  // Получение списка туров
  getAll: async (params?: { limit?: number; offset?: number; city?: string }): Promise<Tour[]> => {
    const response = await api.get<Tour[]>('/tours/', { params });
    return response.data;
  },

  // Получение тура по ID
  getById: async (id: number): Promise<Tour> => {
    const response = await api.get<Tour>(`/tours/${id}`);
    return response.data;
  },

  // Создание тура
  create: async (data: TourCreate): Promise<Tour> => {
    const response = await api.post<Tour>('/tours/', data);
    return response.data;
  },

  // Обновление тура
  update: async (id: number, data: TourUpdate): Promise<Tour> => {
    const response = await api.put<Tour>(`/tours/${id}`, data);
    return response.data;
  },

  // Удаление тура
  delete: async (id: number): Promise<void> => {
    await api.delete(`/tours/${id}`);
  },
};

export default toursApi;
