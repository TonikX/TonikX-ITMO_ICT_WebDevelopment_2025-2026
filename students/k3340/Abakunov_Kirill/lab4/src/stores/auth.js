import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { authAPI } from '@/api'

export const useAuthStore = defineStore('auth', () => {
  const user = ref(JSON.parse(localStorage.getItem('user')) || null)
  const token = ref(localStorage.getItem('token') || null)
  const loading = ref(false)
  const error = ref(null)

  const isAuthenticated = computed(() => !!token.value)

  async function login(credentials) {
    loading.value = true
    error.value = null
    try {
      const response = await authAPI.login(credentials)
      token.value = response.data.auth_token
      localStorage.setItem('token', token.value)
      
      // Получаем данные пользователя
      const userResponse = await authAPI.getCurrentUser()
      user.value = userResponse.data
      localStorage.setItem('user', JSON.stringify(user.value))
      
      return true
    } catch (e) {
      error.value = e.response?.data || 'Ошибка входа'
      return false
    } finally {
      loading.value = false
    }
  }

  async function register(userData) {
    loading.value = true
    error.value = null
    try {
      await authAPI.register(userData)
      // После регистрации автоматически входим
      return await login({
        username: userData.username,
        password: userData.password
      })
    } catch (e) {
      error.value = e.response?.data || 'Ошибка регистрации'
      return false
    } finally {
      loading.value = false
    }
  }

  async function logout() {
    loading.value = true
    try {
      await authAPI.logout()
    } catch (e) {
      // Игнорируем ошибки при выходе
    } finally {
      token.value = null
      user.value = null
      localStorage.removeItem('token')
      localStorage.removeItem('user')
      loading.value = false
    }
  }

  async function updateUser(userData) {
    loading.value = true
    error.value = null
    try {
      const response = await authAPI.updateUser(userData)
      user.value = response.data
      localStorage.setItem('user', JSON.stringify(user.value))
      return true
    } catch (e) {
      error.value = e.response?.data || 'Ошибка обновления'
      return false
    } finally {
      loading.value = false
    }
  }

  async function changePassword(data) {
    loading.value = true
    error.value = null
    try {
      await authAPI.changePassword(data)
      return true
    } catch (e) {
      error.value = e.response?.data || 'Ошибка смены пароля'
      return false
    } finally {
      loading.value = false
    }
  }

  async function fetchUser() {
    if (!token.value) return
    try {
      const response = await authAPI.getCurrentUser()
      user.value = response.data
      localStorage.setItem('user', JSON.stringify(user.value))
    } catch (e) {
      logout()
    }
  }

  return {
    user,
    token,
    loading,
    error,
    isAuthenticated,
    login,
    register,
    logout,
    updateUser,
    changePassword,
    fetchUser,
  }
})
