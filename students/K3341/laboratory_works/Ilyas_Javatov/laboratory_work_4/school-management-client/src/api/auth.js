import axios from 'axios'

const API_URL = process.env.VUE_APP_API_URL || 'http://localhost:8000'

const api = axios.create({
  baseURL: API_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
})

api.interceptors.request.use(
  config => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Token ${token}`
    }
    return config
  },
  error => Promise.reject(error)
)

api.interceptors.response.use(
  response => response,
  error => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token')
      localStorage.removeItem('user')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

api.login = credentials => api.post('/api/auth/token/login/', credentials)
api.register = userData => api.post('/api/auth/users/', userData)
api.logout = () => api.post('/api/auth/token/logout/')
api.getCurrentUser = () => api.get('/api/auth/users/me/')
api.updateProfile = userData => api.patch('/api/auth/users/me/', userData)
api.changePassword = passwords => api.post('/api/auth/users/set_password/', passwords)

export default api