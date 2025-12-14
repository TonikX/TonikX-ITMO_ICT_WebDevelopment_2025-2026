import { ref, computed } from 'vue'
import { authAPI } from '../api/auth'
import { useRouter } from 'vue-router'

const token = ref(localStorage.getItem('token') || null)
const user = ref(null)

export function useAuth() {
  const router = useRouter()

  const isAuthenticated = computed(() => !!token.value)

  const login = async (username, password) => {
    try {
      const response = await authAPI.login({ username, password })
      token.value = response.data.auth_token
      localStorage.setItem('token', token.value)
      await fetchUser()
      router.push('/')
      return { success: true }
    } catch (error) {
      return { success: false, error: error.response?.data || error.message }
    }
  }

  const register = async (data) => {
    try {
      await authAPI.register(data)
      return { success: true }
    } catch (error) {
      return { success: false, error: error.response?.data || error.message }
    }
  }

  const logout = async () => {
    try {
      await authAPI.logout()
    } catch (error) {
      console.error('Logout error:', error)
    }
    token.value = null
    user.value = null
    localStorage.removeItem('token')
    router.push('/login')
  }

  const fetchUser = async () => {
    if (!token.value) return
    try {
      const response = await authAPI.getCurrentUser()
      user.value = response.data
    } catch (error) {
      console.error('Fetch user error:', error)
    }
  }

  if (token.value) {
    fetchUser()
  }

  return {
    token,
    user,
    isAuthenticated,
    login,
    register,
    logout,
    fetchUser
  }
}

