import axios from 'axios'

const API_BASE_URL = 'http://localhost:8000'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Interceptor для добавления токена к запросам
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('auth_token')
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
      localStorage.removeItem('auth_token')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

export const authAPI = {
  login: (username, password) => {
    return api.post('/auth/token/login/', { username, password })
  },
  logout: () => {
    return api.post('/auth/token/logout/')
  },
  register: (username, password, email) => {
    return api.post('/auth/users/', { username, password, email })
  },
  getCurrentUser: () => {
    return api.get('/auth/users/me/')
  },
  updateUser: (data) => {
    return api.patch('/auth/users/me/', data)
  },
  changePassword: (currentPassword, newPassword) => {
    return api.post('/auth/users/set_password/', {
      current_password: currentPassword,
      new_password: newPassword,
    })
  },
}

export const hotelAPI = {
  roomTypes: {
    list: () => api.get('/api/room-types/'),
    get: (id) => api.get(`/api/room-types/${id}/`),
    create: (data) => api.post('/api/room-types/', data),
    update: (id, data) => api.put(`/api/room-types/${id}/`, data),
    patch: (id, data) => api.patch(`/api/room-types/${id}/`, data),
    delete: (id) => api.delete(`/api/room-types/${id}/`),
    stats: () => api.get('/api/room-types/stats/'),
  },
  floors: {
    list: () => api.get('/api/floors/'),
    get: (id) => api.get(`/api/floors/${id}/`),
    create: (data) => api.post('/api/floors/', data),
    update: (id, data) => api.put(`/api/floors/${id}/`, data),
    patch: (id, data) => api.patch(`/api/floors/${id}/`, data),
    delete: (id) => api.delete(`/api/floors/${id}/`),
    stats: () => api.get('/api/floors/stats/'),
  },
  rooms: {
    list: () => api.get('/api/rooms/'),
    get: (id) => api.get(`/api/rooms/${id}/`),
    create: (data) => api.post('/api/rooms/', data),
    update: (id, data) => api.put(`/api/rooms/${id}/`, data),
    patch: (id, data) => api.patch(`/api/rooms/${id}/`, data),
    delete: (id) => api.delete(`/api/rooms/${id}/`),
  },
  guests: {
    list: () => api.get('/api/guests/'),
    get: (id) => api.get(`/api/guests/${id}/`),
    create: (data) => api.post('/api/guests/', data),
    update: (id, data) => api.put(`/api/guests/${id}/`, data),
    patch: (id, data) => api.patch(`/api/guests/${id}/`, data),
    delete: (id) => api.delete(`/api/guests/${id}/`),
  },
  stays: {
    list: () => api.get('/api/stays/'),
    get: (id) => api.get(`/api/stays/${id}/`),
    create: (data) => api.post('/api/stays/', data),
    update: (id, data) => api.put(`/api/stays/${id}/`, data),
    patch: (id, data) => api.patch(`/api/stays/${id}/`, data),
    delete: (id) => api.delete(`/api/stays/${id}/`),
    summary: (date) => {
      const params = date ? { date } : {}
      return api.get('/api/stays/summary/', { params })
    },
  },
  employees: {
    list: () => api.get('/api/employees/'),
    get: (id) => api.get(`/api/employees/${id}/`),
    create: (data) => api.post('/api/employees/', data),
    update: (id, data) => api.put(`/api/employees/${id}/`, data),
    patch: (id, data) => api.patch(`/api/employees/${id}/`, data),
    delete: (id) => api.delete(`/api/employees/${id}/`),
  },
  cleaning: {
    list: () => api.get('/api/cleaning/'),
    get: (id) => api.get(`/api/cleaning/${id}/`),
    create: (data) => api.post('/api/cleaning/', data),
    update: (id, data) => api.put(`/api/cleaning/${id}/`, data),
    patch: (id, data) => api.patch(`/api/cleaning/${id}/`, data),
    delete: (id) => api.delete(`/api/cleaning/${id}/`),
  },
}

export default api

