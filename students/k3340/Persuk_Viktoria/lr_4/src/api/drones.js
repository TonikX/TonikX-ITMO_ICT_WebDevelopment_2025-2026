import apiClient from './axios'

/**
 * API методы для работы с дронами
 */

/**
 * Получить список всех дронов
 * @returns {Promise} Список дронов
 */
export const getDrones = async () => {
  const response = await apiClient.get('/api/drones/')
  return response.data
}

/**
 * Получить детальную информацию о дроне
 * @param {number} droneId - ID дрона
 * @returns {Promise} Данные дрона
 */
export const getDrone = async (droneId) => {
  const response = await apiClient.get(`/api/drones/${droneId}/`)
  return response.data
}

/**
 * Создать новый дрон
 * @param {Object} droneData - Данные дрона
 * @returns {Promise} Созданный дрон
 */
export const createDrone = async (droneData) => {
  const response = await apiClient.post('/api/drones/', droneData)
  return response.data
}

/**
 * Обновить дрон
 * @param {number} droneId - ID дрона
 * @param {Object} droneData - Данные для обновления
 * @returns {Promise} Обновлённый дрон
 */
export const updateDrone = async (droneId, droneData) => {
  const response = await apiClient.patch(`/api/drones/${droneId}/`, droneData)
  return response.data
}

/**
 * Удалить дрон
 * @param {number} droneId - ID дрона
 * @returns {Promise}
 */
export const deleteDrone = async (droneId) => {
  const response = await apiClient.delete(`/api/drones/${droneId}/`)
  return response.data
}

/**
 * Получить полёты конкретного дрона
 * @param {number} droneId - ID дрона
 * @returns {Promise} Список полётов
 */
export const getDroneFlights = async (droneId) => {
  const response = await apiClient.get(`/api/drones/${droneId}/flights/`)
  return response.data
}

/**
 * Получить документы конкретного дрона
 * @param {number} droneId - ID дрона
 * @returns {Promise} Список документов
 */
export const getDroneDocuments = async (droneId) => {
  const response = await apiClient.get(`/api/drones/${droneId}/documents/`)
  return response.data
}
