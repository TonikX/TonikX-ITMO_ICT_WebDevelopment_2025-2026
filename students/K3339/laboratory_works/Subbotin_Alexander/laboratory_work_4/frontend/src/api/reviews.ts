import api from './client';
import type { Review, ReviewCreate, ReviewUpdate } from '@/types';

export const reviewsApi = {
  // Получение отзывов по туру
  getByTour: async (tourId: number, params?: { limit?: number; offset?: number }): Promise<Review[]> => {
    const response = await api.get<Review[]>(`/reviews/tour/${tourId}`, { params });
    return response.data;
  },

  // Получение своего отзыва на тур
  getMyForTour: async (tourId: number): Promise<Review | null> => {
    try {
      const response = await api.get<Review>(`/reviews/my/${tourId}`);
      return response.data;
    } catch {
      return null;
    }
  },

  // Получение отзыва по ID
  getById: async (id: number): Promise<Review> => {
    const response = await api.get<Review>(`/reviews/${id}`);
    return response.data;
  },

  // Создание отзыва
  create: async (data: ReviewCreate): Promise<Review> => {
    const response = await api.post<Review>('/reviews/', data);
    return response.data;
  },

  // Обновление отзыва
  update: async (id: number, data: ReviewUpdate): Promise<Review> => {
    const response = await api.put<Review>(`/reviews/${id}`, data);
    return response.data;
  },

  // Удаление отзыва
  delete: async (id: number): Promise<void> => {
    await api.delete(`/reviews/${id}`);
  },
};

export default reviewsApi;
