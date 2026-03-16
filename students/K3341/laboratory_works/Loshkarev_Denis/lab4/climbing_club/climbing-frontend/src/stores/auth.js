import { defineStore } from 'pinia'
import api from '../api'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: localStorage.getItem('token') || '',
    user: null,
  }),
  actions: {
    async login(username, password) {
      try {
        const response = await api.post('auth/token/login/', { username, password })
        this.token = response.data.auth_token
        localStorage.setItem('token', this.token)
        return true
      } catch (error) {
        console.error('Ошибка входа:', error)
        return false
      }
    },
    logout() {
      this.token = ''
      localStorage.removeItem('token') 
    }
  }
})
