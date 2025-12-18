import { defineStore } from 'pinia'
import router from '../router'
import { loginRequest, logoutRequest, meRequest, registerRequest } from '../api/auth'
import { setAuthToken, setUnauthorizedHandler } from '../api/http'
import type { LoginPayload, RegisterPayload, User } from '../types/auth'

const STORAGE_KEY = 'auth_token'

interface AuthState {
  token: string | null
  user: User | null
  initialized: boolean
  loading: boolean
  error: string | null
}

export const useAuthStore = defineStore('auth', {
  state: (): AuthState => ({
    token: localStorage.getItem(STORAGE_KEY),
    user: null,
    initialized: false,
    loading: false,
    error: null,
  }),
  getters: {
    isAdmin: (state) => !!state.user?.is_staff,
    brokerId: (state) => state.user?.broker_id ?? null,
  },
  actions: {
    async init() {
      if (this.initialized) return
      if (this.token) {
        setAuthToken(this.token)
        try {
          await this.fetchMe()
        } catch {
          await this.logout(true)
        }
      }
      setUnauthorizedHandler(() => this.logout(true))
      this.initialized = true
    },
    async login(payload: LoginPayload) {
      this.loading = true
      this.error = null
      try {
        const token = await loginRequest(payload)
        this.token = token
        localStorage.setItem(STORAGE_KEY, token)
        setAuthToken(token)
        await this.fetchMe()
      } catch (err: unknown) {
        this.error = this.getErrorMessage(err)
        throw err
      } finally {
        this.loading = false
      }
    },
    async register(payload: RegisterPayload) {
      this.loading = true
      this.error = null
      try {
        await registerRequest(payload)
        await this.login({ username: payload.username, password: payload.password })
      } catch (err: unknown) {
        this.error = this.getErrorMessage(err)
        throw err
      } finally {
        this.loading = false
      }
    },
    async logout(silent = false) {
      try {
        if (!silent && this.token) {
          await logoutRequest()
        }
      } catch {
        // ignore
      } finally {
        this.token = null
        this.user = null
        localStorage.removeItem(STORAGE_KEY)
        setAuthToken(null)
        if (!silent) {
          router.push({ name: 'login' })
        }
      }
    },
    async fetchMe() {
      if (!this.token) return null
      const data = await meRequest()
      this.user = data
      return data
    },
    getErrorMessage(err: unknown) {
      if (typeof err === 'object' && err && 'response' in err) {
        const resp = (err as any).response
        if (resp?.data) {
          if (typeof resp.data === 'string') return resp.data
          if (resp.data?.detail) return resp.data.detail
          if (resp.data?.non_field_errors) return resp.data.non_field_errors.join(', ')
        }
      }
      return 'Request failed'
    },
  },
})

