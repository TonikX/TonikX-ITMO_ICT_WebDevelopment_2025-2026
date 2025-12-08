import { defineStore } from 'pinia'
import axios from 'axios'

const API_BASE = 'http://127.0.0.1:8000'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: localStorage.getItem('access_token') || null,
    user: null,
    loading: false,
    error: null,
  }),

  getters: {
    isAuthenticated: (state) => !!state.token,
    isAdmin: (state) => !!state.user?.is_staff,
  },

  actions: {
    async login(username, password) {
      this.loading = true
      this.error = null
      try {
        const response = await axios.post(`${API_BASE}/auth/jwt/create/`, {
          username,
          password,
        })

        this.token = response.data.access
        localStorage.setItem('access_token', this.token)

        await this.fetchUser()
      } catch (error) {
        console.error('Login error', error)
        this.error = 'Неверное имя пользователя или пароль'
        throw error
      } finally {
        this.loading = false
      }
    },

    async register({ username, password, re_password }) {
      this.loading = true
      this.error = null
      try {
        await axios.post(`${API_BASE}/auth/users/`, {
          username,
          password,
          re_password,
        })
        await this.login(username, password)
      } catch (error) {
        console.error('Register error', error)
        this.error = 'Ошибка регистрации (проверьте данные)'
        throw error
      } finally {
        this.loading = false
      }
    },

    async fetchUser() {
      if (!this.token) return
      try {
        const response = await axios.get(`${API_BASE}/auth/users/me/`, {
          headers: {
            Authorization: `Bearer ${this.token}`,
          },
        })
        this.user = response.data
      } catch (error) {
        console.error('Fetch user error', error)
      }
    },

    logout() {
      this.token = null
      this.user = null
      this.error = null
      localStorage.removeItem('access_token')
    },
  },
})
