import api from './client';
import type { User, UserProfile, Token, UserCreate } from '@/types';

export const authApi = {
  // Регистрация нового пользователя
  register: async (data: UserCreate): Promise<User> => {
    const response = await api.post<User>('/auth/register', data);
    return response.data;
  },

  // Авторизация пользователя (OAuth2 формат)
  login: async (username: string, password: string): Promise<Token> => {
    const formData = new URLSearchParams();
    formData.append('username', username);
    formData.append('password', password);
    
    const response = await api.post<Token>('/auth/login', formData, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
    });
    return response.data;
  },

  // Получение текущего пользователя
  getCurrentUser: async (): Promise<User> => {
    const response = await api.get<User>('/auth/me');
    return response.data;
  },

  // Получение профиля пользователя
  getProfile: async (): Promise<UserProfile> => {
    const response = await api.get<UserProfile>('/auth/me/profile');
    return response.data;
  },

  // Обновление профиля пользователя
  updateProfile: async (data: { date_of_birth?: string }): Promise<UserProfile> => {
    const response = await api.put<UserProfile>('/auth/me/profile', data);
    return response.data;
  },

  // Обновление данных пользователя (username, email)
  updateUser: async (data: { username?: string; email?: string }): Promise<User> => {
    const response = await api.put<User>('/auth/me', data);
    return response.data;
  },

  // Смена пароля
  changePassword: async (currentPassword: string, newPassword: string): Promise<void> => {
    await api.put('/auth/me/password', {
      current_password: currentPassword,
      new_password: newPassword,
    });
  },
};

export default authApi;
