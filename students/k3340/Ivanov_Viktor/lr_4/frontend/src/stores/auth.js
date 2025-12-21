import { defineStore } from 'pinia'
import api from '../services/api'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: localStorage.getItem('token') || null,
    user: null,
    loading: false,
    error: null,
  }),
  getters: {
    isAuthenticated: (state) => Boolean(state.token),
  },
  actions: {
    setToken(token) {
      this.token = token
      if (token) {
        localStorage.setItem('token', token)
      } else {
        localStorage.removeItem('token')
      }
    },
    async login(payload) {
      this.loading = true
      this.error = null
      try {
        const { data } = await api.post('/api/auth/token/login/', payload)
        this.setToken(data.auth_token)
        await this.fetchMe()
      } catch (err) {
        this.error = err.response?.data || 'Не удалось войти'
        throw err
      } finally {
        this.loading = false
      }
    },
    async register(payload) {
      this.loading = true
      this.error = null
      try {
        await api.post('/api/auth/users/', payload)
        await this.login({ username: payload.username, password: payload.password })
      } catch (err) {
        this.error = err.response?.data || 'Не удалось зарегистрироваться'
        throw err
      } finally {
        this.loading = false
      }
    },
    async logout() {
      try {
        if (this.token) {
          await api.post('/api/auth/token/logout/')
        }
      } catch (e) {
        // игнорируем сетевые ошибки при логауте
      } finally {
        this.setToken(null)
        this.user = null
      }
    },
    async fetchMe() {
      if (!this.token) return
      try {
        const { data } = await api.get('/api/auth/users/me/')
        this.user = data
      } catch (err) {
        this.setToken(null)
        this.user = null
      }
    },
  },
})


