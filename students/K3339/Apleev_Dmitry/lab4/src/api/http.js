import axios from 'axios'

// базовая настройка axios
// базовый url пустой, чтобы в dev все запросы шли через прокси vite
export const apiClient = axios.create({
  baseURL: '',
  timeout: 10000
})

// добавляем токен авторизации в каждый запрос, если он есть
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('auth_token')
    if (token) {
      config.headers.Authorization = `Token ${token}`
    }
    return config
  },
  (error) => Promise.reject(error)
)

