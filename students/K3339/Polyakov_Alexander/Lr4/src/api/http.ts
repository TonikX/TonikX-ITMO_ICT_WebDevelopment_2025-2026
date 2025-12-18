import axios from 'axios'

let authToken: string | null = null
let onUnauthorized: (() => void) | null = null

export const setAuthToken = (token: string | null) => {
  authToken = token
}

export const setUnauthorizedHandler = (handler: (() => void) | null) => {
  onUnauthorized = handler
}

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000/',
})

api.interceptors.request.use((config) => {
  if (authToken) {
    config.headers = config.headers || {}
    config.headers.Authorization = `Token ${authToken}`
  }
  return config
})

api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401 && onUnauthorized) {
      onUnauthorized()
    }
    return Promise.reject(error)
  },
)

export default api

