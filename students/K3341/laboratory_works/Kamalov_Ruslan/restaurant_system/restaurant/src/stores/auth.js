import { ref, computed } from 'vue'
import { authAPI } from '@/services/api'

const user = ref(null)
const token = ref(localStorage.getItem('token'))

export const useAuthStore = () => {
  const isAuthenticated = computed(() => !!token.value)

  const login = async (credentials) => {
    try {
      const response = await authAPI.login(credentials)
      token.value = response.data.auth_token
      localStorage.setItem('token', token.value)
      await getCurrentUser()
      return { success: true }
    } catch (error) {
      return { success: false, error: error.response?.data }
    }
  }

  const register = async (userData) => {
    try {
      await authAPI.register(userData)
      return { success: true }
    } catch (error) {
      return { success: false, error: error.response?.data }
    }
  }

  const logout = async () => {
    try {
      if (token.value) {
        await authAPI.logout()
      }
    } catch (error) {
      console.error('Logout error:', error)
    } finally {
      token.value = null
      user.value = null
      localStorage.removeItem('token')
    }
  }

  const getCurrentUser = async () => {
    try {
      const response = await authAPI.getCurrentUser()
      user.value = response.data
    } catch (error) {
      console.error('Get current user error:', error)
      logout()
    }
  }

  const initAuth = async () => {
    if (token.value) {
      await getCurrentUser()
    }
  }

  return {
    user: computed(() => user.value),
    token: computed(() => token.value),
    isAuthenticated,
    login,
    register,
    logout,
    getCurrentUser,
    initAuth
  }
}