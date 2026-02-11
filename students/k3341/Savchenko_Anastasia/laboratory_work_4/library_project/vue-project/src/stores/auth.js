import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import axios from 'axios'

export const useAuthStore = defineStore('auth', () => {
  // Состояние
  const token = ref(localStorage.getItem('access_token') || null)
  const user = ref(null)
  const loading = ref(false)
  const error = ref(null)

  // Геттеры
  const isAuthenticated = computed(() => !!token.value)
  const isAdmin = computed(() => !!user.value?.is_staff)

  // Действия
  async function login(username, password) {
    loading.value = true
    error.value = null

    try {
      const response = await axios.post('http://127.0.0.1:8000/auth/token/login/', {
        username,
        password,
      })

      token.value = response.data.auth_token
      localStorage.setItem('access_token', token.value)

      await fetchUser()
    } catch (err) {
      error.value = 'Неверное имя пользователя или пароль'
      throw err
    } finally {
      loading.value = false
    }
  }

  async function register(userData) {
    loading.value = true
    error.value = null

    try {
      await axios.post('http://127.0.0.1:8000/auth/users/', userData)
      // После регистрации автоматически логинимся
      await login(userData.username, userData.password)
    } catch (err) {
      error.value = 'Ошибка регистрации'
      throw err
    } finally {
      loading.value = false
    }
  }

  async function fetchUser() {
    if (!token.value) return

    try {
      const response = await axios.get('http://127.0.0.1:8000/auth/users/me/', {
        headers: {
          Authorization: `Token ${token.value}`,
        },
      })
      user.value = response.data
    } catch (err) {
      console.error('Ошибка загрузки пользователя:', err)
      logout()
    }
  }

  function logout() {
    token.value = null
    user.value = null
    error.value = null
    localStorage.removeItem('access_token')
  }

  return {
    // Состояние
    token,
    user,
    loading,
    error,

    // Геттеры
    isAuthenticated,
    isAdmin,

    // Действия
    login,
    register,
    fetchUser,
    logout,
  }
})