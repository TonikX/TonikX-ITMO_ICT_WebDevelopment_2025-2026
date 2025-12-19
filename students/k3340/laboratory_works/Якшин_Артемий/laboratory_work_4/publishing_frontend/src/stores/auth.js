import { defineStore } from 'pinia'
import { authApi } from '@/services/api'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,
    token: localStorage.getItem('auth_token') || null,
    loading: false,
    error: null,
  }),

  getters: {
    isAuthenticated: (state) => !!state.token,
  },

  actions: {
    async login(credentials) {
      this.loading = true
      this.error = null
      try {
        const response = await authApi.login(credentials)
        this.token = response.data.auth_token
        localStorage.setItem('auth_token', this.token)
        await this.fetchProfile()
        return { success: true }
      } catch (error) {
        this.error = error.response?.data?.non_field_errors?.[0] || 
                     error.response?.data?.detail ||
                     'Ошибка входа. Проверьте учётные данные.'
        return { success: false, error: this.error }
      } finally {
        this.loading = false
      }
    },

    async register(userData) {
      this.loading = true
      this.error = null
      try {
        await authApi.register(userData)
        return { success: true }
      } catch (error) {
        const errors = error.response?.data
        if (errors) {
          const errorMessages = []
          for (const [field, messages] of Object.entries(errors)) {
            if (Array.isArray(messages)) {
              errorMessages.push(...messages)
            } else {
              errorMessages.push(messages)
            }
          }
          this.error = errorMessages.join('. ')
        } else {
          this.error = 'Ошибка регистрации. Попробуйте позже.'
        }
        return { success: false, error: this.error }
      } finally {
        this.loading = false
      }
    },

    async logout() {
      try {
        if (this.token) {
          await authApi.logout()
        }
      } catch (error) {
        console.error('Logout error:', error)
      } finally {
        this.token = null
        this.user = null
        localStorage.removeItem('auth_token')
      }
    },

    async fetchProfile() {
      if (!this.token) return

      try {
        const response = await authApi.getProfile()
        this.user = response.data
      } catch (error) {
        console.error('Error fetching profile:', error)
        if (error.response?.status === 401) {
          this.logout()
        }
      }
    },

    async updateProfile(data) {
      this.loading = true
      this.error = null
      try {
        const response = await authApi.updateProfile(data)
        this.user = response.data
        return { success: true }
      } catch (error) {
        this.error = error.response?.data?.detail || 'Ошибка обновления профиля'
        return { success: false, error: this.error }
      } finally {
        this.loading = false
      }
    },

    async changePassword(data) {
      this.loading = true
      this.error = null
      try {
        await authApi.changePassword(data)
        return { success: true }
      } catch (error) {
        const errors = error.response?.data
        if (errors) {
          const errorMessages = []
          for (const messages of Object.values(errors)) {
            if (Array.isArray(messages)) {
              errorMessages.push(...messages)
            } else {
              errorMessages.push(messages)
            }
          }
          this.error = errorMessages.join('. ')
        } else {
          this.error = 'Ошибка смены пароля'
        }
        return { success: false, error: this.error }
      } finally {
        this.loading = false
      }
    },

    initializeAuth() {
      if (this.token) {
        this.fetchProfile()
      }
    }
  }
})

