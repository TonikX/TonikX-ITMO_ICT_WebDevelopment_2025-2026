import { ref } from 'vue'
import { apiLogin, apiLogout, apiGetCurrentUser } from '../api'

// здесь хранится простое состояние авторизации

const token = ref(localStorage.getItem('auth_token') || '')
const user = ref(null)
const loading = ref(false)
const error = ref('')

export function useAuthStore() {
  // вход в систему
  const login = async (credentials) => {
    loading.value = true
    error.value = ''
    try {
      const response = await apiLogin(credentials)
      const authToken = response.data.auth_token
      token.value = authToken
      localStorage.setItem('auth_token', authToken)
      await fetchCurrentUser()
    } catch (e) {
      error.value = 'не удалось войти, проверьте данные'
      throw e
    } finally {
      loading.value = false
    }
  }

  // выход из системы
  const logout = async () => {
    try {
      await apiLogout()
    } catch (e) {
      // здесь можно игнорировать ошибку выхода
    } finally {
      token.value = ''
      user.value = null
      localStorage.removeItem('auth_token')
    }
  }

  // получение информации о текущем пользователе
  const fetchCurrentUser = async () => {
    if (!token.value) {
      user.value = null
      return
    }
    try {
      const response = await apiGetCurrentUser()
      user.value = response.data
    } catch (e) {
      // если токен невалиден — очищаем
      token.value = ''
      user.value = null
      localStorage.removeItem('auth_token')
    }
  }

  return {
    token,
    user,
    loading,
    error,
    login,
    logout,
    fetchCurrentUser
  }
}

