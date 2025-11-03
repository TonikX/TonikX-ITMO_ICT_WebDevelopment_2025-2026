import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import api from '@/services/api'

export const useAuthStore = defineStore('auth', () => {
  const token = ref(localStorage.getItem('token') || null)
  const user = ref(JSON.parse(localStorage.getItem('user') || 'null'))

  const isAuthenticated = computed(() => !!token.value)

  async function login(credentials) {
    try {
      const response = await api.post('/auth/jwt/create/', credentials)
      token.value = response.data.access
      user.value = { username: credentials.username }
      localStorage.setItem('token', response.data.access)
      localStorage.setItem('user', JSON.stringify(user.value))
      return { success: true }
    } catch (error) {
      return { success: false, error: error.response?.data?.detail || 'Ошибка входа' }
    }
  }

  async function register(userData) {
    try {
      await api.post('/auth/users/', userData)
      return { success: true }
    } catch (error) {
      return { success: false, error: error.response?.data || 'Ошибка регистрации' }
    }
  }

  async function logout() {
    token.value = null
    user.value = null
    localStorage.removeItem('token')
    localStorage.removeItem('user')
  }

  async function getCurrentUser() {
    try {
      const response = await api.get('/auth/users/me/')
      user.value = response.data
      localStorage.setItem('user', JSON.stringify(user.value))
      return response.data
    } catch (error) {
      console.error('Ошибка получения пользователя:', error)
      return null
    }
  }

  return {
    token,
    user,
    isAuthenticated,
    login,
    register,
    logout,
    getCurrentUser
  }
})

