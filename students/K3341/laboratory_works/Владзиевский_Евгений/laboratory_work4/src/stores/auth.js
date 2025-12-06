import { reactive } from 'vue'
import { loginUser, registerUser, getMe, updateProfile } from '../api/client'
import { authStorage, clearTokens } from '../api/http'

const state = reactive({
  user: null,
  loading: false,
  ready: false,
})

export const useAuthState = () => state

export const isAuthenticated = () => Boolean(state.user || authStorage.getAccessToken())
export const currentUserId = () => state.user?.id || authStorage.getUserId()

export async function initAuth() {
  if (!authStorage.getAccessToken() && !authStorage.getRefreshToken()) {
    state.ready = true
    return
  }
  state.loading = true
  try {
    state.user = await getMe()
  } catch (e) {
    console.warn('Failed to restore session', e)
    clearTokens()
    state.user = null
  } finally {
    state.loading = false
    state.ready = true
  }
}

export async function signIn(credentials) {
  state.loading = true
  try {
    await loginUser(credentials)
    state.user = await getMe()
    return state.user
  } finally {
    state.loading = false
    state.ready = true
  }
}

export async function signUp(payload) {
  state.loading = true
  try {
    await registerUser(payload)
    state.user = await getMe()
    return state.user
  } finally {
    state.loading = false
    state.ready = true
  }
}

export function logout() {
  clearTokens()
  state.user = null
}

export async function saveProfile(form) {
  state.loading = true
  try {
    const user = await updateProfile(form)
    state.user = user
    return user
  } finally {
    state.loading = false
  }
}
