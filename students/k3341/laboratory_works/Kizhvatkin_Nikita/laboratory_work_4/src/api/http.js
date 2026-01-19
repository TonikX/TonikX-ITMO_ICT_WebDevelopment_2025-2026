import axios from 'axios'
import { useAuthStore } from '../stores/auth'

const baseURL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api'

export const http = axios.create({
  baseURL,
  timeout: 20000,
})

http.interceptors.request.use((config) => {
  const auth = useAuthStore()
  if (!auth.token) auth.hydrate()
  const hasAuthHeader =
    !!config.headers?.Authorization ||
    !!config.headers?.authorization
  if (!hasAuthHeader && auth.token) {
    config.headers = config.headers || {}
    config.headers.Authorization = `Token ${auth.token}`
  }
  return config
})

http.interceptors.response.use(
  (resp) => resp,
  (error) => {
    const auth = useAuthStore()
    const status = error?.response?.status
    const detail = error?.response?.data?.detail
    if (
      status === 401 ||
      status === 403 ||
      detail?.toLowerCase().includes('token') ||
      detail?.toLowerCase().includes('credentials')
    ) {
      auth.token = null
      auth.user = null
      auth.persist()
    }
    throw error
  }
)
