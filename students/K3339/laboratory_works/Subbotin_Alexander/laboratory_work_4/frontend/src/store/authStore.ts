import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import type { User } from '@/types';
import { authApi } from '@/api';

interface AuthState {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  error: string | null;
  
  // Actions
  login: (username: string, password: string) => Promise<void>;
  register: (username: string, email: string, password: string) => Promise<void>;
  logout: () => void;
  fetchUser: () => Promise<void>;
  clearError: () => void;
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set, get) => ({
      user: null,
      token: null,
      isAuthenticated: false,
      isLoading: false,
      error: null,

      login: async (username: string, password: string) => {
        set({ isLoading: true, error: null });
        try {
          const tokenData = await authApi.login(username, password);
          localStorage.setItem('token', tokenData.access_token);
          set({ token: tokenData.access_token, isAuthenticated: true });
          
          // Fetch user data after login
          await get().fetchUser();
        } catch (error: unknown) {
          const err = error as { response?: { data?: { detail?: string } } };
          const message = err.response?.data?.detail || 'Ошибка авторизации';
          set({ error: message, isLoading: false });
          throw error;
        }
      },

      register: async (username: string, email: string, password: string) => {
        set({ isLoading: true, error: null });
        try {
          await authApi.register({ username, email, password });
          // После регистрации автоматически логиним пользователя
          await get().login(username, password);
        } catch (error: unknown) {
          const err = error as { response?: { data?: { detail?: string } } };
          const message = err.response?.data?.detail || 'Ошибка регистрации';
          set({ error: message, isLoading: false });
          throw error;
        }
      },

      logout: () => {
        localStorage.removeItem('token');
        set({ 
          user: null, 
          token: null, 
          isAuthenticated: false,
          error: null 
        });
      },

      fetchUser: async () => {
        const token = get().token || localStorage.getItem('token');
        if (!token) {
          set({ isLoading: false });
          return;
        }

        set({ isLoading: true });
        try {
          const user = await authApi.getCurrentUser();
          set({ user, isAuthenticated: true, isLoading: false });
        } catch {
          // Если не удалось получить пользователя, очищаем токен
          localStorage.removeItem('token');
          set({ 
            user: null, 
            token: null, 
            isAuthenticated: false, 
            isLoading: false 
          });
        }
      },

      clearError: () => set({ error: null }),
    }),
    {
      name: 'auth-storage',
      partialize: (state) => ({ 
        token: state.token, 
        isAuthenticated: state.isAuthenticated 
      }),
    }
  )
);
