import axios from 'axios'

const API_URL = 'http://localhost:8000'

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json'
  }
})

// Interceptor для добавления токена к запросам
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

// API методы для аутентификации
export const authAPI = {
  register: (userData) => api.post('/auth/users/', userData),
  login: (credentials) => api.post('/auth/token/login/', credentials),
  logout: () => api.post('/auth/token/logout/'),
  getCurrentUser: () => api.get('/auth/users/me/')
}

// API методы для работы с данными
export const dataAPI = {
  // Статистика по маркам самолетов
  getTopMark: () => api.get('/api/mark/top/'),
  getAllMarks: () => api.get('/api/mark/all/'),
  
  // Рейсы
  getFlightsWithLowOccupancy: (filledLessThan) => 
    api.post('/api/routes/pick/', { filled_less_than: filledLessThan }),
  getAvailableSeats: (flightId) => api.get(`/api/flights/${flightId}/available_seats/`),
  
  // Самолеты
  getPlanesInRepair: () => api.get('/api/planes/in_repair/'),
  
  // Сотрудники
  getEmployeesCount: () => api.get('/api/employees/count/')
}

export default api