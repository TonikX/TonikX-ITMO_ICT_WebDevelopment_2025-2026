import api from './api'

export const serviceRequestsService = {
  async getServiceRequests(params = {}) {
    const response = await api.get('/api/service-requests/', { params })
    return response.data
  },

  async getServiceRequest(id) {
    const response = await api.get(`/api/service-requests/${id}/`)
    return response.data
  },

  async createServiceRequest(data) {
    const response = await api.post('/api/service-requests/', data)
    return response.data
  },

  async updateServiceRequest(id, data) {
    const response = await api.patch(`/api/service-requests/${id}/`, data)
    return response.data
  },

  async deleteServiceRequest(id) {
    const response = await api.delete(`/api/service-requests/${id}/`)
    return response.data
  },

  async assignWorker(id, workerId) {
    const response = await api.post(`/api/service-requests/${id}/assign_worker/`, {
      worker_id: workerId,
    })
    return response.data
  },

  async changeStatus(id, status) {
    const response = await api.post(`/api/service-requests/${id}/change_status/`, {
      status,
    })
    return response.data
  },

  async addComment(id, comment) {
    const response = await api.post(`/api/service-requests/${id}/add_comment/`, {
      comment,
    })
    return response.data
  },

  async getMyRequests(params = {}) {
    const response = await api.get('/api/service-requests/my_requests/', { params })
    return response.data
  },

  async getAssignedToMe(params = {}) {
    const response = await api.get('/api/service-requests/assigned_to_me/', { params })
    return response.data
  },

  async getStatistics() {
    const response = await api.get('/api/service-requests/statistics/')
    return response.data
  },
}

