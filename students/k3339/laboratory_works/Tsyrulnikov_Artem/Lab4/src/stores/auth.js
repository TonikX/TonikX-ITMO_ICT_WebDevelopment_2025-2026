import { defineStore } from 'pinia'
import api from '@/api'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,
    isAuth: !!localStorage.getItem('access')
  }),
  actions: {
    async login(username, password) {
      const { data } = await api.post('/auth/jwt/create/', { username, password })
      localStorage.setItem('access', data.access)
      localStorage.setItem('refresh', data.refresh)
      this.isAuth = true
      await this.fetchUser()
    },
    async register(username, password) {
      await api.post('/auth/users/', { username, password })
      await this.login(username, password)
    },
    async fetchUser() {
      if (!this.isAuth) return
      const { data } = await api.get('/auth/users/me/')
      this.user = data
    },
    async updateUser(userData) {
      const { data } = await api.patch('/auth/users/me/', userData)
      this.user = data
    },
    logout() {
      localStorage.clear()
      this.user = null
      this.isAuth = false
    }
  }
})
