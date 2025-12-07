import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import api from '@/services/api'

interface User {
  id: number
  username: string
  email?: string
}

export const useAuthStore = defineStore('auth', () => {
  const user = ref<User | null>(null)
  const token = ref<string | null>(localStorage.getItem('auth_token'))
  const loading = ref(false)
  const error = ref<string | null>(null)

  const isAuthenticated = computed(() => !!token.value)

  async function init() {
    if (token.value) {
      try {
        const userData = await api.getCurrentUser()
        user.value = userData
      } catch {
        logout()
      }
    }
  }

  async function login(username: string, password: string) {
    loading.value = true
    error.value = null
    try {
      const response = await api.login(username, password)
      token.value = response.auth_token
      localStorage.setItem('auth_token', response.auth_token)

      const userData = await api.getCurrentUser()
      user.value = userData

      return { success: true }
    } catch (err: unknown) {
      const axiosError = err as { response?: { data?: { non_field_errors?: string[]; message?: string } } }
      error.value = axiosError.response?.data?.non_field_errors?.[0] ||
                   axiosError.response?.data?.message ||
                   'Ошибка входа. Проверьте правильность данных.'
      return { success: false, error: error.value }
    } finally {
      loading.value = false
    }
  }

  async function register(username: string, password: string, password_retype: string) {
    loading.value = true
    error.value = null
    try {
      await api.register(username, password, password_retype)
      return await login(username, password)
    } catch (err: unknown) {
      const axiosError = err as { response?: { data?: { username?: string[]; password?: string[]; non_field_errors?: string[] } } }
      const errorMessages: string[] = []

      if (axiosError.response?.data) {
        const data = axiosError.response.data
        if (data.username) errorMessages.push(`Имя пользователя: ${data.username.join(', ')}`)
        if (data.password) errorMessages.push(`Пароль: ${data.password.join(', ')}`)
        if (data.non_field_errors) errorMessages.push(data.non_field_errors.join(', '))
      }

      error.value = errorMessages.length > 0
        ? errorMessages.join(' ')
        : 'Ошибка регистрации. Попробуйте снова.'
      return { success: false, error: error.value }
    } finally {
      loading.value = false
    }
  }

  async function updateProfile(data: { username?: string; email?: string }) {
    loading.value = true
    error.value = null
    try {
      const updatedUser = await api.updateUser(data)
      user.value = updatedUser
      return { success: true }
    } catch (err: unknown) {
      const axiosError = err as { response?: { data?: { message?: string; [key: string]: unknown } } }
      error.value = axiosError.response?.data?.message ||
                   (axiosError.response?.data ? Object.values(axiosError.response.data).flat().join(', ') : '') ||
                   'Ошибка обновления профиля'
      return { success: false, error: error.value }
    } finally {
      loading.value = false
    }
  }

  async function changePassword(current_password: string, new_password: string, re_new_password: string) {
    loading.value = true
    error.value = null
    try {
      await api.changePassword(current_password, new_password, re_new_password)
      return { success: true }
    } catch (err: unknown) {
      const axiosError = err as { response?: { data?: { current_password?: string[]; new_password?: string[]; non_field_errors?: string[] } } }
      const errorMessages: string[] = []

      if (axiosError.response?.data) {
        const data = axiosError.response.data
        if (data.current_password) errorMessages.push(`Текущий пароль: ${data.current_password.join(', ')}`)
        if (data.new_password) errorMessages.push(`Новый пароль: ${data.new_password.join(', ')}`)
        if (data.non_field_errors) errorMessages.push(data.non_field_errors.join(', '))
      }

      error.value = errorMessages.length > 0
        ? errorMessages.join(' ')
        : 'Ошибка смены пароля'
      return { success: false, error: error.value }
    } finally {
      loading.value = false
    }
  }

  function logout() {
    token.value = null
    user.value = null
    localStorage.removeItem('auth_token')
  }

  return {
    user,
    token,
    loading,
    error,
    isAuthenticated,
    init,
    login,
    register,
    updateProfile,
    changePassword,
    logout,
  }
})

