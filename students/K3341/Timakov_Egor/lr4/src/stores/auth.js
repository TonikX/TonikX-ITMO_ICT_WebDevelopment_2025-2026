import { defineStore } from 'pinia'
import api from '../plugins/axios'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: localStorage.getItem('auth_token') || null,
    user: JSON.parse(localStorage.getItem('user') || 'null')
  }),

  getters: {
    isAuthenticated: (state) => !!state.token,
    currentUser: (state) => state.user
  },

  actions: {
    async login(credentials) {
      try {
        const response = await api.post('/auth/token/login/', credentials)
        const token = response.data.auth_token
        
        this.token = token
        localStorage.setItem('auth_token', token)
        
        // Получаем информацию о пользователе
        await this.fetchUser()
        
        return { success: true }
      } catch (error) {
        return {
          success: false,
          error: error.response?.data || { message: 'Ошибка входа' }
        }
      }
    },

    async register(userData) {
      try {
        await api.post('/auth/users/', userData)
        // После регистрации автоматически входим
        return await this.login({
          username: userData.username,
          password: userData.password
        })
      } catch (error) {
        return {
          success: false,
          error: error.response?.data || { message: 'Ошибка регистрации' }
        }
      }
    },

    async fetchUser() {
      try {
        const response = await api.get('/auth/users/me/')
        this.user = response.data
        localStorage.setItem('user', JSON.stringify(response.data))
      } catch (error) {
        console.error('Ошибка получения данных пользователя:', error)
      }
    },

    async updateUser(userData) {
      try {
        const response = await api.patch('/auth/users/me/', userData)
        this.user = response.data
        localStorage.setItem('user', JSON.stringify(response.data))
        return { success: true }
      } catch (error) {
        return {
          success: false,
          error: error.response?.data || { message: 'Ошибка обновления данных' }
        }
      }
    },

    async changePassword(passwordData) {
      try {
        await api.post('/auth/users/set_password/', passwordData)
        return { success: true }
      } catch (error) {
        return {
          success: false,
          error: error.response?.data || { message: 'Ошибка смены пароля' }
        }
      }
    },

    async logout() {
      try {
        await api.post('/auth/token/logout/')
      } catch (error) {
        console.error('Ошибка выхода:', error)
      } finally {
        this.token = null
        this.user = null
        localStorage.removeItem('auth_token')
        localStorage.removeItem('user')
      }
    }
  }
})
