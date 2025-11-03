import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Добавляем токен к каждому запросу
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Обработка ошибок авторизации
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

export const readingRoomsAPI = {
  getAll: () => api.get('/reading-rooms/'),
  getById: (id) => api.get(`/reading-rooms/${id}/`),
  create: (data) => api.post('/reading-rooms/', data),
  update: (id, data) => api.put(`/reading-rooms/${id}/`, data),
  delete: (id) => api.delete(`/reading-rooms/${id}/`),
  getFreeReadingRooms: (datetime) => api.get(`/reading-rooms/free/?on=${datetime}`),
  getReadersInPeriod: (id, start, end) => api.get(`/reading-rooms/${id}/readers/?start=${start}&end=${end}`),
}

export const readersAPI = {
  getAll: () => api.get('/readers/'),
  getById: (id) => api.get(`/readers/${id}/`),
  create: (data) => api.post('/readers/', data),
  update: (id, data) => api.put(`/readers/${id}/`, data),
  delete: (id) => api.delete(`/readers/${id}/`),
  getCountByPhone: (phone) => api.get(`/readers/count-by-phone/?phone=${phone}`),
  getLibrarianOnWeekday: (id, weekday) => api.get(`/readers/${id}/librarian/?weekday=${weekday}`),
  getCoReaders: (id, start, end) => api.get(`/readers/${id}/co-readers/?start=${start}&end=${end}`),
}

export const reservationsAPI = {
  getAll: () => api.get('/reservations/'),
  getById: (id) => api.get(`/reservations/${id}/`),
  create: (data) => api.post('/reservations/', data),
  update: (id, data) => api.put(`/reservations/${id}/`, data),
  delete: (id) => api.delete(`/reservations/${id}/`),
}

export const librariansAPI = {
  getAll: () => api.get('/librarians/'),
  getById: (id) => api.get(`/librarians/${id}/`),
  create: (data) => api.post('/librarians/', data),
  update: (id, data) => api.put(`/librarians/${id}/`, data),
  delete: (id) => api.delete(`/librarians/${id}/`),
  fire: (id) => api.post(`/librarians/${id}/fire/`),
  hire: (id) => api.post(`/librarians/${id}/hire/`),
}

export const schedulesAPI = {
  getAll: () => api.get('/schedules/'),
  getById: (id) => api.get(`/schedules/${id}/`),
  create: (data) => api.post('/schedules/', data),
  update: (id, data) => api.put(`/schedules/${id}/`, data),
  delete: (id) => api.delete(`/schedules/${id}/`),
}

export const reportsAPI = {
  getQuarterReport: (quarter) => api.get(`/reports/quarter/?quarter=${quarter}`),
}

export default api
