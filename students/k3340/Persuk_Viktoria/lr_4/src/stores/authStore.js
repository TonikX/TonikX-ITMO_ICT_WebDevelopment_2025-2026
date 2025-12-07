import { defineStore } from 'pinia'
import * as authAPI from '@/api/auth'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: null,
    user: null,
    isLoading: false,
  }),

  getters: {
    isAuthenticated: (state) => !!state.token && !!state.user,
  },

  actions: {
    async login(username, password) {
      this.isLoading = true
      try {
        const data = await authAPI.login(username, password)
        console.log('Login data:', data)
        // Djoser возвращает { auth_token: "..." }
        const token = data.auth_token
        console.log('Token extracted:', token)
        if (!token) {
          return { success: false, error: 'Токен не получен от сервера' }
        }
        this.token = token
        // Загружаем пользователя с явным токеном
        const user = await authAPI.getCurrentUser(token)
        this.user = user
        return { success: true }
      } catch (error) {
        console.error('Login error:', error)
        const message =
          error.response?.data?.non_field_errors?.[0] ||
          error.response?.data?.detail ||
          'Ошибка входа'
        return { success: false, error: message }
      } finally {
        this.isLoading = false
      }
    },

    async register(username, email, password) {
      this.isLoading = true
      try {
        await authAPI.register(username, email, password)
        // После регистрации сразу логинимся
        return await this.login(username, password)
      } catch (error) {
        console.error('Register error:', error)
        const errors = error.response?.data || {}
        let message = 'Ошибка регистрации'
        if (errors.username) {
          message = Array.isArray(errors.username) ? errors.username[0] : errors.username
        } else if (errors.email) {
          message = Array.isArray(errors.email) ? errors.email[0] : errors.email
        } else if (errors.password) {
          message = Array.isArray(errors.password) ? errors.password[0] : errors.password
        }
        return { success: false, error: message }
      } finally {
        this.isLoading = false
      }
    },

    async logout() {
      if (this.token) {
        try {
          await authAPI.logout(this.token)
        } catch (e) {
          // игнорируем ошибки logout
        }
      }
      this.token = null
      this.user = null
    },
  },

  persist: {
    enabled: true,
    strategies: [
      {
        key: 'auth',
        storage: localStorage,
        paths: ['token', 'user'],
      },
    ],
  },
})
