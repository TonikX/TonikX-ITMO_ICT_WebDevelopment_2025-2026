import api from './api'

export const buildingsService = {
  async getBuildings(params = {}) {
    const response = await api.get('/api/buildings/', { params })
    return response.data
  },

  async getBuilding(id) {
    const response = await api.get(`/api/buildings/${id}/`)
    return response.data
  },

  async createBuilding(data) {
    const response = await api.post('/api/buildings/', data)
    return response.data
  },

  async updateBuilding(id, data) {
    const response = await api.patch(`/api/buildings/${id}/`, data)
    return response.data
  },

  async deleteBuilding(id) {
    const response = await api.delete(`/api/buildings/${id}/`)
    return response.data
  },

  async getStatistics() {
    const response = await api.get('/api/buildings/statistics/')
    return response.data
  },
}

