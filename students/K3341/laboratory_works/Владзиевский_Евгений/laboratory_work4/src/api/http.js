import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:80'
const IMAGE_HOST = API_BASE_URL

const ACCESS_KEY = 'access_token'
const REFRESH_KEY = 'refresh_token'
const USER_KEY = 'user_id'

const authStorage = {
  getAccessToken: () => localStorage.getItem(ACCESS_KEY),
  getRefreshToken: () => localStorage.getItem(REFRESH_KEY),
  getUserId: () => localStorage.getItem(USER_KEY),
  setTokens: ({ access_token, refresh_token, user_id }) => {
    if (access_token) localStorage.setItem(ACCESS_KEY, access_token)
    if (refresh_token) localStorage.setItem(REFRESH_KEY, refresh_token)
    if (user_id) localStorage.setItem(USER_KEY, String(user_id))
  },
  clear: () => {
    localStorage.removeItem(ACCESS_KEY)
    localStorage.removeItem(REFRESH_KEY)
    localStorage.removeItem(USER_KEY)
  },
}

const api = axios.create({
  baseURL: API_BASE_URL,
})

let refreshPromise = null

async function performRefresh() {
  const refreshToken = authStorage.getRefreshToken()
  if (!refreshToken) throw new Error('No refresh token')
  const res = await axios.post(
    `${API_BASE_URL}/refresh`,
    null,
    {
      headers: { Authorization: `Bearer ${refreshToken}` },
    },
  )
  authStorage.setTokens(res.data)
  return res.data
}

api.interceptors.request.use((config) => {
  const token = authStorage.getAccessToken()
  if (token) {
    config.headers = {
      ...config.headers,
      Authorization: `Bearer ${token}`,
    }
  }
  return config
})

api.interceptors.response.use(
  (res) => res,
  async (error) => {
    const status = error.response?.status
    const originalRequest = error.config

    if (status === 401 && !originalRequest.__isRetry) {
      if (!refreshPromise) {
        refreshPromise = performRefresh().finally(() => {
          refreshPromise = null
        })
      }
      try {
        const data = await refreshPromise
        originalRequest.__isRetry = true
        originalRequest.headers = {
          ...(originalRequest.headers || {}),
          Authorization: `Bearer ${data.access_token}`,
        }
        return api(originalRequest)
      } catch (refreshError) {
        authStorage.clear()
        return Promise.reject(refreshError)
      }
    }
    return Promise.reject(error)
  },
)

export { api, authStorage, API_BASE_URL }
export const setTokens = (payload) => authStorage.setTokens(payload)
export const clearTokens = () => authStorage.clear()
const normalizedImageHost = IMAGE_HOST.replace(/\/+$/, '')
export const buildImageUrl = (hash) => `${normalizedImageHost}/image/${hash}`
