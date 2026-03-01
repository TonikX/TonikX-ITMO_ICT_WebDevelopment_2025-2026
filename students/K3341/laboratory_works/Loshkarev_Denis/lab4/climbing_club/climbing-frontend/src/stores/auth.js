import { defineStore } from 'pinia'
import api from '../api'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token:    localStorage.getItem('token')    || '',
    username: localStorage.getItem('username') || '',
  }),
  actions: {
    async login(username, password) {
      try {
        const response = await api.post('auth/token/login/', { username, password })
        this.token    = response.data.auth_token
        this.username = username
        localStorage.setItem('token',    this.token)
        localStorage.setItem('username', username)
        return true
      } catch (error) {
        console.error('Ошибка входа:', error)
        return false
      }
    },
    logout() {
      this.token    = ''
      this.username = ''
      localStorage.removeItem('token')
      localStorage.removeItem('username')
    }
  }
})