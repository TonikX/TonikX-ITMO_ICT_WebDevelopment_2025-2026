import { defineStore } from 'pinia';
import api from '../api/axios';

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: localStorage.getItem('token') || null,
    isAuthenticated: !!localStorage.getItem('token'),
  }),
  actions: {
    async login(credentials) {
      // Интерфейс 1: Вход
      const response = await api.post('/auth/token/login/', credentials);
      this.token = response.data.auth_token;
      this.isAuthenticated = true;
      localStorage.setItem('token', this.token);
    },
    async register(userData) {
      // Интерфейс 2: Регистрация
      await api.post('/auth/users/', userData);
    },
    logout() {
      // Интерфейс 3: Выход
      this.token = null;
      this.isAuthenticated = false;
      localStorage.removeItem('token');
    }
  }
});