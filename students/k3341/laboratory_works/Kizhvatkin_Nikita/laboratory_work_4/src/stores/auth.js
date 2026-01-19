import { defineStore } from 'pinia'
import { http } from '../api/http'
import { endpoints } from '../api/endpoints'

const STORAGE_KEY = 'airline_auth_token_v1'

function loadSaved() {
  try {
    return JSON.parse(localStorage.getItem(STORAGE_KEY) || '{}')
  } catch {
    return {}
  }
}

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: null,
    user: null,
  }),
  getters: {
    isAuthenticated: (s) => !!s.token,
  },
  actions: {
    hydrate() {
      const saved = loadSaved()
      this.token = saved.token || null
      this.user = saved.user || null
    },
    persist() {
      localStorage.setItem(
        STORAGE_KEY,
        JSON.stringify({
          token: this.token,
          user: this.user,
        })
      )
    },
    async login({ username, password }) {
      const res = await http.post(endpoints.tokenLogin, { username, password })
      const tok = res?.data?.auth_token
      if (!tok) throw new Error('Не удалось получить токен авторизации')
      this.token = tok
      this.persist()
      await this.fetchCurrentUser()
    },
    async fetchCurrentUser() {
      const res = await http.get(endpoints.currentUser)
      this.user = res.data
      this.persist()
      return res.data
    },
    async updateProfile(payload) {
      const res = await http.patch(endpoints.currentUser, payload)
      this.user = res.data
      this.persist()
      return res.data
    },
    async register(payload) {
      const res = await http.post(endpoints.register, payload)
      return res.data
    },
    async logout() {
      if (this.token) {
        try {
          await http.post(endpoints.tokenLogout)
        }
        catch {
        }
      }
      this.token = null
      this.user = null
      this.persist()
    },
  },
})
