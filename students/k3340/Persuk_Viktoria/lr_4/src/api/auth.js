import axios from 'axios'

const BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

// Создаём чистый экземпляр axios без interceptors и defaults
const cleanAxios = axios.create({
  baseURL: BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

/**
 * Вход пользователя
 */
export const login = async (username, password) => {
  const response = await cleanAxios.post('/auth/token/login/', {
    username,
    password,
  })
  return response.data // { auth_token: "..." }
}

/**
 * Регистрация нового пользователя
 */
export const register = async (username, email, password) => {
  const payload = { username, password }
  if (email) {
    payload.email = email
  }
  const response = await cleanAxios.post('/auth/users/', payload)
  return response.data
}

/**
 * Получение информации о текущем пользователе
 */
export const getCurrentUser = async (token) => {
  const response = await cleanAxios.get('/auth/users/me/', {
    headers: {
      'Authorization': `Token ${token}`,
    },
  })
  return response.data
}

/**
 * Выход (аннулирование токена)
 */
export const logout = async (token) => {
  await cleanAxios.post('/auth/token/logout/', null, {
    headers: {
      'Authorization': `Token ${token}`,
    },
  })
}
