import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { authAPI } from '@/services/api'

export const useAuthStore = defineStore('auth', () => {
  const token = ref(localStorage.getItem('token') || null)
  const user = ref(null)

  const isAuthenticated = computed(() => !!token.value)

  const login = async (credentials) => {
    try {
      const response = await authAPI.login(credentials)
      token.value = response.data.auth_token
      localStorage.setItem('token', response.data.auth_token)
      await fetchUser()
      return { success: true }
    } catch (error) {
      return { success: false, error: error.response?.data || 'Ошибка входа' }
    }
  }

  const register = async (userData) => {
    try {
      await authAPI.register(userData)
      return { success: true }
    } catch (error) {
      return { success: false, error: error.response?.data || 'Ошибка регистрации' }
    }
  }

  const logout = async () => {
    try {
      await authAPI.logout()
    } catch (error) {
      console.error('Logout error:', error)
    } finally {
      token.value = null
      user.value = null
      localStorage.removeItem('token')
    }
  }

  const fetchUser = async () => {
    try {
      const response = await authAPI.getCurrentUser()
      user.value = response.data
    } catch (error) {
      console.error('Fetch user error:', error)
      logout()
    }
  }

  if (token.value) {
    fetchUser()
  }

  return {
    token,
    user,
    isAuthenticated,
    login,
    register,
    logout,
    fetchUser
  }
})