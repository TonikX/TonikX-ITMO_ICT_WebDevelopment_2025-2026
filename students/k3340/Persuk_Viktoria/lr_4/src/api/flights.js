import apiClient from './axios'

/**
 * API методы для работы с полётами
 */

/**
 * Получить список всех полётов
 * @returns {Promise} Список полётов
 */
export const getFlights = async () => {
  const response = await apiClient.get('/api/flights/')
  return response.data
}

/**
 * Получить детальную информацию о полёте
 * @param {number} flightId - ID полёта
 * @returns {Promise} Данные полёта
 */
export const getFlight = async (flightId) => {
  const response = await apiClient.get(`/api/flights/${flightId}/`)
  return response.data
}

/**
 * Создать новый полёт
 * @param {Object} flightData - Данные полёта
 * @param {number} droneId - ID дрона (опционально, если создаётся через /drones/{id}/flights/)
 * @returns {Promise} Созданный полёт
 */
export const createFlight = async (flightData, droneId = null) => {
  const url = droneId
    ? `/api/drones/${droneId}/flights/`
    : '/api/flights/'
  const response = await apiClient.post(url, flightData)
  return response.data
}

/**
 * Обновить полёт
 * @param {number} flightId - ID полёта
 * @param {Object} flightData - Данные для обновления
 * @returns {Promise} Обновлённый полёт
 */
export const updateFlight = async (flightId, flightData) => {
  const response = await apiClient.patch(`/api/flights/${flightId}/`, flightData)
  return response.data
}

/**
 * Удалить полёт
 * @param {number} flightId - ID полёта
 * @returns {Promise}
 */
export const deleteFlight = async (flightId) => {
  const response = await apiClient.delete(`/api/flights/${flightId}/`)
  return response.data
}

/**
 * Получить логи конкретного полёта
 * @param {number} flightId - ID полёта
 * @returns {Promise} Список логов
 */
export const getFlightLogs = async (flightId) => {
  const response = await apiClient.get(`/api/flights/${flightId}/logs/`)
  return response.data
}
