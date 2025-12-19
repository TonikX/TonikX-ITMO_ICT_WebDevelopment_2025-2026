import { defineStore } from 'pinia'
import { login as apiLogin, register as apiRegister, getProfile as apiGetProfile } from '@/api/auth'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: localStorage.getItem('authToken') || null,
    user: null,
    loading: false,
    profileLoading: false,
    error: null
  }),

  getters: {
    isAuthenticated: (state) => !!state.token,
    role: (state) => state.user?.role || null
  },

  actions: {
    async login(username, password) {
      this.loading = true
      try {
        const data = await apiLogin(username, password)
        this.token = data.auth_token
        localStorage.setItem('authToken', this.token)
        await this.fetchProfile()
        this.error = null
      } catch (err) {
        this.error = err.response?.data?.detail || 'Ошибка авторизации'
        this.token = null
        localStorage.removeItem('authToken')
      } finally {
        this.loading = false
      }
    },

    async register(userData) {
      this.loading = true
      try {
        await apiRegister(userData)
        await this.login(userData.username, userData.password)
        this.error = null
      } catch (err) {
        this.error = err.response?.data || 'Ошибка регистрации'
      } finally {
        this.loading = false
      }
    },

    async fetchProfile() {
      if (!this.token) return
      this.profileLoading = true
      try {
        this.user = await apiGetProfile()
      } catch (err) {
        this.logout()
      } finally {
        this.profileLoading = false
      }
    },

    logout() {
      this.token = null
      this.user = null
      localStorage.removeItem('authToken')
    }
  }
})