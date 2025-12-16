import { ref } from 'vue'
import api from './api/api'

export const isLoggedIn = ref(false)

export function initAuthFromStorage() {
  const token = localStorage.getItem('auth_token')
  if (token) {
    setAuthToken(token)
  } else {
    isLoggedIn.value = false
  }
}

export function setAuthToken(token) {
  if (token) {
    localStorage.setItem('auth_token', token)
    api.defaults.headers.common['Authorization'] = `Token ${token}`
    isLoggedIn.value = true
  } else {
    localStorage.removeItem('auth_token')
    delete api.defaults.headers.common['Authorization']
    isLoggedIn.value = false
  }
}
