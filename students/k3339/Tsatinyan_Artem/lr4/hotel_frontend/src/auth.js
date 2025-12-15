import api from './api/api'

const TOKEN_KEY = 'auth_token'

export function setAuthToken(token) {
  localStorage.setItem(TOKEN_KEY, token)
  api.defaults.headers.common['Authorization'] = `Token ${token}`
}

export function clearAuthToken() {
  localStorage.removeItem(TOKEN_KEY)
  delete api.defaults.headers.common['Authorization']
}

export function initAuthFromStorage() {
  const token = localStorage.getItem(TOKEN_KEY)
  if (token) {
    api.defaults.headers.common['Authorization'] = `Token ${token}`
  }
}
