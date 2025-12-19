import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import api from '@/api/client'

export const useAuthStore = defineStore('auth', () => {
  const token = ref(localStorage.getItem('access_token') || null)
  const refreshToken = ref(localStorage.getItem('refresh_token') || null)
  const user = ref(JSON.parse(localStorage.getItem('user') || 'null'))

  const isAuthenticated = computed(() => !!token.value)

  const login = async (username, password) => {
    try {
      const response = await api.post('/auth/login', { username, password })
      token.value = response.data.access_token
      refreshToken.value = response.data.refresh_token
      
      // Если user приходит в ответе, используем его, иначе создаем из токена
      if (response.data.user) {
        user.value = response.data.user
      } else {
        // Создаем минимальный объект пользователя
        user.value = {
          username: username,
          role: 'user' // Будет обновлено при следующем запросе
        }
      }
      
      localStorage.setItem('access_token', token.value)
      localStorage.setItem('refresh_token', refreshToken.value)
      localStorage.setItem('user', JSON.stringify(user.value))
      
      api.defaults.headers.common['Authorization'] = `Bearer ${token.value}`
      return response.data
    } catch (error) {
      throw error
    }
  }

  const register = async (username, email, password, role) => {
    try {
      const response = await api.post('/auth/register', { username, email, password, role })
      
      // Если регистрация успешна и вернулись токены, автоматически логиним пользователя
      if (response.data.access_token) {
        token.value = response.data.access_token
        refreshToken.value = response.data.refresh_token
        user.value = response.data.user
        
        localStorage.setItem('access_token', token.value)
        localStorage.setItem('refresh_token', refreshToken.value)
        localStorage.setItem('user', JSON.stringify(user.value))
        
        api.defaults.headers.common['Authorization'] = `Bearer ${token.value}`
      }
      
      return response.data
    } catch (error) {
      throw error
    }
  }

  const logout = () => {
    token.value = null
    refreshToken.value = null
    user.value = null
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
    localStorage.removeItem('user')
    delete api.defaults.headers.common['Authorization']
  }

  const initAuth = () => {
    if (token.value) {
      api.defaults.headers.common['Authorization'] = `Bearer ${token.value}`
    }
  }

  return {
    token,
    refreshToken,
    user,
    isAuthenticated,
    login,
    register,
    logout,
    initAuth
  }
})

