import apiClient from './axios'

/**
 * API методы для работы с профилем пользователя
 */

/**
 * Получение профиля текущего пользователя
 * @returns {Promise} Данные профиля
 */
export const getProfile = async () => {
  const response = await apiClient.get('/api/profile/')
  return response.data
}

/**
 * Обновление профиля текущего пользователя
 * @param {FormData|Object} profileData - Данные профиля (display_name, bio, avatar)
 * @returns {Promise} Обновленные данные профиля
 */
export const updateProfile = async (profileData) => {
  const response = await apiClient.patch('/api/profile/', profileData, {
    headers: {
      'Content-Type': profileData instanceof FormData
        ? 'multipart/form-data'
        : 'application/json',
    },
  })
  return response.data
}

/**
 * Получение профиля другого пользователя
 * @param {number} userId - ID пользователя
 * @returns {Promise} Данные профиля
 */
export const getUserProfile = async (userId) => {
  const response = await apiClient.get(`/api/users/${userId}/profile/`)
  return response.data
}
