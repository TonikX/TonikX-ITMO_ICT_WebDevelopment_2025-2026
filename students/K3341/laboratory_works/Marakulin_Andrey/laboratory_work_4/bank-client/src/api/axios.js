import axios from 'axios';

const api = axios.create({
  baseURL: 'http://127.0.0.1:8000', // Адрес твоего сервера Django
});

// Перехватчик: автоматически добавляет токен в каждый запрос
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Token ${token}`;
  }
  return config;
});

export default api;