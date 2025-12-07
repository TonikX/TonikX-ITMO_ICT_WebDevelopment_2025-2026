import api from './api'

export const meterReadingsService = {
  async getMeterReadings(params = {}) {
    const response = await api.get('/api/meter-readings/', { params })
    return response.data
  },

  async getMeterReading(id) {
    const response = await api.get(`/api/meter-readings/${id}/`)
    return response.data
  },

  async createMeterReading(data) {
    const response = await api.post('/api/meter-readings/', data)
    return response.data
  },

  async updateMeterReading(id, data) {
    const response = await api.patch(`/api/meter-readings/${id}/`, data)
    return response.data
  },

  async deleteMeterReading(id) {
    const response = await api.delete(`/api/meter-readings/${id}/`)
    return response.data
  },

  async getStatistics() {
    const response = await api.get('/api/meter-readings/statistics/')
    return response.data
  },
}

