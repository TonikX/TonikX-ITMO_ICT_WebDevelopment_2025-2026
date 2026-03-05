import { defineStore } from 'pinia'
import api from '../utils/api'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,
    token: localStorage.getItem('token') || null
  }),
  getters: {
    isAuthenticated: (s) => !!s.token
  },
  actions: {
    async login(username, password) {
      const res = await api.post('/auth/jwt/create/', { username, password })
      this.token = res.data.access
      localStorage.setItem('token', this.token)
      api.setAuth(this.token)
      const me = await api.get('/auth/users/me/')
      this.user = me.data
    },
    async logout() {
      this.token = null
      this.user = null
      localStorage.removeItem('token')
      api.setAuth(null)
    },
    async fetchMe() {
      if (!this.token) return
      const me = await api.get('/auth/users/me/')
      this.user = me.data
    }
    ,
    async updateProfile(data) {
      if (!this.token) throw new Error('Not authenticated')
      const res = await api.patch('/auth/users/me/', data)
      this.user = res.data
      return res
    },
    async changePassword(current_password, new_password) {
      if (!this.token) throw new Error('Not authenticated')
      try {
        const res = await api.post('/auth/users/set_password/', { current_password, new_password })
        return res
      } catch (e) {
        const res = await api.patch('/auth/users/me/', { password: new_password })
        return res
      }
    }
  }
})