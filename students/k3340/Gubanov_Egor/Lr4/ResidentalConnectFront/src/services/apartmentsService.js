import api from './api'

export const apartmentsService = {
  async getApartments(params = {}) {
    const response = await api.get('/api/apartments/', { params })
    return response.data
  },

  async getApartment(id) {
    const response = await api.get(`/api/apartments/${id}/`)
    return response.data
  },

  async createApartment(data) {
    const response = await api.post('/api/apartments/', data)
    return response.data
  },

  async updateApartment(id, data) {
    const response = await api.patch(`/api/apartments/${id}/`, data)
    return response.data
  },

  async deleteApartment(id) {
    const response = await api.delete(`/api/apartments/${id}/`)
    return response.data
  },
}

