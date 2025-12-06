import apiClient from './axios'

/**
 * API методы для аутентификации через Djoser
 */

/**
 * Вход пользователя
 * Примечание: Djoser настроен на LOGIN_FIELD: "username", но также может принимать email
 * как username (если backend это поддерживает). Поле отправляется как "username".
 * @param {string} usernameOrEmail - Username или email пользователя
 * @param {string} password - Пароль
 * @returns {Promise} JWT токены (access и refresh)
 */
export const login = async (usernameOrEmail, password) => {
  // Djoser с LOGIN_FIELD: "username" ожидает поле "username"
  // Но можно передать email в поле username, если backend это поддерживает
  const response = await apiClient.post('/auth/jwt/create/', {
    username: usernameOrEmail, // Отправляем как username (может быть email)
    password,
  })
  return response.data
}

/**
 * Регистрация нового пользователя
 * @param {string} email - Email пользователя
 * @param {string} username - Имя пользователя (опционально, генерируется из email если не указано)
 * @param {string} password - Пароль
 * @param {string} re_password - Подтверждение пароля
 * @returns {Promise} Данные созданного пользователя
 */
export const register = async (email, username, password, re_password) => {
  const response = await apiClient.post('/auth/users/', {
    email,
    username: username || undefined,
    password,
    re_password,
  })
  return response.data
}

/**
 * Обновление JWT токена
 * @param {string} refreshToken - Refresh токен
 * @returns {Promise} Новый access токен
 */
export const refreshToken = async (refreshToken) => {
  const response = await apiClient.post('/auth/jwt/refresh/', {
    refresh: refreshToken,
  })
  return response.data
}

/**
 * Получение информации о текущем пользователе
 * @returns {Promise} Данные пользователя
 */
export const getCurrentUser = async () => {
  const response = await apiClient.get('/auth/users/me/')
  return response.data
}

/**
 * Обновление данных текущего пользователя
 * @param {Object} userData - Данные для обновления (email, username)
 * @returns {Promise} Обновленные данные пользователя
 */
export const updateCurrentUser = async (userData) => {
  const response = await apiClient.patch('/auth/users/me/', userData)
  return response.data
}

/**
 * Изменение пароля текущего пользователя
 * @param {string} currentPassword - Текущий пароль
 * @param {string} newPassword - Новый пароль
 * @param {string} reNewPassword - Подтверждение нового пароля
 * @returns {Promise}
 */
export const changePassword = async (currentPassword, newPassword, reNewPassword) => {
  const response = await apiClient.post('/auth/users/set_password/', {
    current_password: currentPassword,
    new_password: newPassword,
    re_new_password: reNewPassword,
  })
  return response.data
}
