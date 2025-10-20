import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Добавляем токен к каждому запросу
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Обработка ошибок авторизации
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      localStorage.removeItem('user');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export const authAPI = {
  login: (credentials) => api.post('/auth/jwt/create/', credentials),
  logout: () => api.post('/auth/jwt/blacklist/'),
  register: (userData) => api.post('/auth/users/', userData),
  getCurrentUser: () => api.get('/auth/users/me/'),
};

export const roomsAPI = {
  getAll: () => api.get('/rooms/'),
  getById: (id) => api.get(`/rooms/${id}/`),
  create: (data) => api.post('/rooms/', data),
  update: (id, data) => api.put(`/rooms/${id}/`, data),
  delete: (id) => api.delete(`/rooms/${id}/`),
  getFreeRooms: (date) => api.get(`/rooms/free/?on=${date}`),
  getClientsInPeriod: (id, start, end) => api.get(`/rooms/${id}/clients/?start=${start}&end=${end}`),
};

export const clientsAPI = {
  getAll: () => api.get('/clients/'),
  getById: (id) => api.get(`/clients/${id}/`),
  create: (data) => api.post('/clients/', data),
  update: (id, data) => api.put(`/clients/${id}/`, data),
  delete: (id) => api.delete(`/clients/${id}/`),
  getCountByCity: (city) => api.get(`/clients/count-by-city/?city=${city}`),
  getCleanerOnWeekday: (id, weekday) => api.get(`/clients/${id}/cleaner/?weekday=${weekday}`),
  getCoStayers: (id, start, end) => api.get(`/clients/${id}/co-stayers/?start=${start}&end=${end}`),
};

export const staysAPI = {
  getAll: () => api.get('/stays/'),
  getById: (id) => api.get(`/stays/${id}/`),
  create: (data) => api.post('/stays/', data),
  update: (id, data) => api.put(`/stays/${id}/`, data),
  delete: (id) => api.delete(`/stays/${id}/`),
};

export const employeesAPI = {
  getAll: () => api.get('/employees/'),
  getById: (id) => api.get(`/employees/${id}/`),
  create: (data) => api.post('/employees/', data),
  update: (id, data) => api.put(`/employees/${id}/`, data),
  delete: (id) => api.delete(`/employees/${id}/`),
  fire: (id) => api.post(`/employees/${id}/fire/`),
  hire: (id) => api.post(`/employees/${id}/hire/`),
};

export const schedulesAPI = {
  getAll: () => api.get('/schedules/'),
  getById: (id) => api.get(`/schedules/${id}/`),
  create: (data) => api.post('/schedules/', data),
  update: (id, data) => api.put(`/schedules/${id}/`, data),
  delete: (id) => api.delete(`/schedules/${id}/`),
};

export const reportsAPI = {
  getQuarterReport: (quarter) => api.get(`/reports/quarter/?quarter=${quarter}`),
};

export default api;
