import apiClient from './axios'

/**
 * API методы для работы с документами дронов
 */

/**
 * Получить список всех документов
 * @returns {Promise} Список документов
 */
export const getDocuments = async () => {
  const response = await apiClient.get('/api/documents/')
  return response.data
}

/**
 * Получить детальную информацию о документе
 * @param {number} documentId - ID документа
 * @returns {Promise} Данные документа
 */
export const getDocument = async (documentId) => {
  const response = await apiClient.get(`/api/documents/${documentId}/`)
  return response.data
}

/**
 * Создать новый документ
 * @param {Object} documentData - Данные документа
 * @param {number} droneId - ID дрона (опционально, если создаётся через /drones/{id}/documents/)
 * @returns {Promise} Созданный документ
 */
export const createDocument = async (documentData, droneId = null) => {
  const url = droneId
    ? `/api/drones/${droneId}/documents/`
    : '/api/documents/'
  const response = await apiClient.post(url, documentData)
  return response.data
}

/**
 * Обновить документ
 * @param {number} documentId - ID документа
 * @param {Object} documentData - Данные для обновления
 * @returns {Promise} Обновлённый документ
 */
export const updateDocument = async (documentId, documentData) => {
  const response = await apiClient.patch(`/api/documents/${documentId}/`, documentData)
  return response.data
}

/**
 * Удалить документ
 * @param {number} documentId - ID документа
 * @returns {Promise}
 */
export const deleteDocument = async (documentId) => {
  const response = await apiClient.delete(`/api/documents/${documentId}/`)
  return response.data
}
