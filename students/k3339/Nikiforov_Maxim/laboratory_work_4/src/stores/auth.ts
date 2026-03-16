import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import * as authApi from '../shared/api/auth'
import { getStoredToken, setToken } from '../shared/api/client'
import type { User } from '../shared/api/auth'

export const useAuthStore = defineStore('auth', () => {
  const token = ref<string | null>(getStoredToken())
  const user = ref<User | null>(null)

  const isAuthenticated = computed(() => !!token.value)

  async function initUser() {
    const t = getStoredToken()
    token.value = t
    if (!t) {
      user.value = null
      return
    }
    user.value = await authApi.fetchMe()
  }

  async function login(username: string, password: string) {
    const data = await authApi.login({ username, password })
    token.value = data.auth_token
    await initUser()
  }

  async function logout() {
    try {
      await authApi.logout()
    } finally {
      setToken(null)
      token.value = null
      user.value = null
    }
  }

  async function register(username: string, password: string, re_password: string) {
    await authApi.register({ username, password, re_password })
  }

  async function updateProfile(payload: authApi.UpdateMePayload) {
    user.value = await authApi.updateMe(payload)
    return user.value
  }

  return {
    token,
    user,
    isAuthenticated,
    initUser,
    login,
    logout,
    register,
    updateProfile,
  }
})
