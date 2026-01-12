import api from './index'

export const analyticsApi = {
  // Получить доступные таблицы для агрегации
  getAvailableTables() {
    return api.get('/available-tables/')
  },
  
  // Получить сводку продаж по модели
  getSalesSummary(modelName, params = {}) {
    return api.get(`/sales-summary/${modelName}/`, { params })
  }
}