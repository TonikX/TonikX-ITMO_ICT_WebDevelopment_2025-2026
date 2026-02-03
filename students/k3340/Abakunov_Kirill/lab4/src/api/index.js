import axios from 'axios'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Interceptor для добавления токена авторизации
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Token ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Interceptor для обработки ошибок
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token')
      localStorage.removeItem('user')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

// Auth API
export const authAPI = {
  login: (credentials) => api.post('/api/auth/token/login/', credentials),
  logout: () => api.post('/api/auth/token/logout/'),
  register: (userData) => api.post('/api/auth/users/', userData),
  getCurrentUser: () => api.get('/api/auth/users/me/'),
  updateUser: (userData) => api.patch('/api/auth/users/me/', userData),
  changePassword: (data) => api.post('/api/auth/users/set_password/', data),
}

// Rooms API
export const roomsAPI = {
  getAll: (params) => api.get('/api/rooms/', { params }),
  getById: (id) => api.get(`/api/rooms/${id}/`),
  create: (data) => api.post('/api/rooms/', data),
  update: (id, data) => api.put(`/api/rooms/${id}/`, data),
  delete: (id) => api.delete(`/api/rooms/${id}/`),
  getAvailable: () => api.get('/api/rooms/available/'),
  getGuestsHistory: (id, params) => api.get(`/api/rooms/${id}/guests_history/`, { params }),
}

// Guests API
export const guestsAPI = {
  getAll: (params) => api.get('/api/guests/', { params }),
  getById: (id) => api.get(`/api/guests/${id}/`),
  create: (data) => api.post('/api/guests/', data),
  update: (id, data) => api.put(`/api/guests/${id}/`, data),
  delete: (id) => api.delete(`/api/guests/${id}/`),
  getCurrent: () => api.get('/api/guests/current/'),
  getFromCity: (city) => api.get('/api/guests/from_city/', { params: { city } }),
  checkIn: (data) => api.post('/api/guests/check_in/', data),
  checkOut: (id, data) => api.patch(`/api/guests/${id}/check_out/`, data),
  getCleaningStaff: (id, weekday) => api.get(`/api/guests/${id}/cleaning_staff/`, { params: { weekday } }),
  getConcurrentGuests: (id, params) => api.get(`/api/guests/${id}/concurrent_guests/`, { params }),
}

// Staff API
export const staffAPI = {
  getAll: (params) => api.get('/api/staff/', { params }),
  getById: (id) => api.get(`/api/staff/${id}/`),
  create: (data) => api.post('/api/staff/', data),
  update: (id, data) => api.put(`/api/staff/${id}/`, data),
  delete: (id) => api.delete(`/api/staff/${id}/`),
  getActive: () => api.get('/api/staff/active/'),
  hire: (data) => api.post('/api/staff/hire/', data),
  fire: (id, data) => api.patch(`/api/staff/${id}/fire/`, data),
}

// Schedules API
export const schedulesAPI = {
  getAll: (params) => api.get('/api/schedules/', { params }),
  getById: (id) => api.get(`/api/schedules/${id}/`),
  create: (data) => api.post('/api/schedules/', data),
  update: (id, data) => api.put(`/api/schedules/${id}/`, data),
  delete: (id) => api.delete(`/api/schedules/${id}/`),
  getByFloor: (floor) => api.get('/api/schedules/by_floor/', { params: { floor } }),
  getByWeekday: (weekday) => api.get('/api/schedules/by_weekday/', { params: { weekday } }),
}

// Reports API
export const reportsAPI = {
  getQuarterly: (year, quarter) => api.get('/api/reports/quarterly/', { params: { year, quarter } }),
}

export default api
