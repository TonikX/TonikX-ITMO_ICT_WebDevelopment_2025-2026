import axios from 'axios'
import { useAuthStore } from '../stores/auth'

const api = axios.create({
  baseURL: 'http://127.0.0.1:8002',
  withCredentials: true,
})

// Всегда просим JSON
api.defaults.headers.common['Accept'] = 'application/json'
api.defaults.headers.common['Content-Type'] = 'application/json'

api.interceptors.request.use((config) => {
  const auth = useAuthStore()
  if (auth?.token) {
    config.headers.Authorization = `Token ${auth.token}`
  }
  return config
})

export default api


