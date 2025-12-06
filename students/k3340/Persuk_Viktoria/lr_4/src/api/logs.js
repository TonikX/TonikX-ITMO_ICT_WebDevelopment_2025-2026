import apiClient from './axios'

/**
 * API методы для работы с логами полётов
 */

/**
 * Получить список всех логов
 * @returns {Promise} Список логов
 */
export const getLogs = async () => {
  const response = await apiClient.get('/api/logs/')
  return response.data
}

/**
 * Получить детальную информацию о логе
 * @param {number} logId - ID лога
 * @returns {Promise} Данные лога
 */
export const getLog = async (logId) => {
  const response = await apiClient.get(`/api/logs/${logId}/`)
  return response.data
}

/**
 * Создать новый лог
 * @param {Object} logData - Данные лога
 * @param {number} flightId - ID полёта (опционально, если создаётся через /flights/{id}/logs/)
 * @returns {Promise} Созданный лог
 */
export const createLog = async (logData, flightId = null) => {
  const url = flightId
    ? `/api/flights/${flightId}/logs/`
    : '/api/logs/'
  const response = await apiClient.post(url, logData)
  return response.data
}

/**
 * Обновить лог
 * @param {number} logId - ID лога
 * @param {Object} logData - Данные для обновления
 * @returns {Promise} Обновлённый лог
 */
export const updateLog = async (logId, logData) => {
  const response = await apiClient.patch(`/api/logs/${logId}/`, logData)
  return response.data
}

/**
 * Удалить лог
 * @param {number} logId - ID лога
 * @returns {Promise}
 */
export const deleteLog = async (logId) => {
  const response = await apiClient.delete(`/api/logs/${logId}/`)
  return response.data
}
