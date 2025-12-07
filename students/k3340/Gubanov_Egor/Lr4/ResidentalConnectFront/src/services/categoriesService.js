import api from './api'

export const categoriesService = {
  async getCategories(params = {}) {
    const response = await api.get('/api/categories/', { params })
    return response.data
  },

  async getCategory(id) {
    const response = await api.get(`/api/categories/${id}/`)
    return response.data
  },
}

