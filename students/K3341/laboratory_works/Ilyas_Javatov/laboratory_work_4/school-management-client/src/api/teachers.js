import api from './auth'

export default {
  getTeachers(params = {}) {
    return api.get('/api/teachers/', { params })
  },

  getTeacher(id) {
    return api.get(`/api/teachers/${id}/`)
  },

  createTeacher(data) {
    return api.post('/api/teachers/', data)
  },

  updateTeacher(id, data) {
    return api.put(`/api/teachers/${id}/`, data)
  },

  deleteTeacher(id) {
    return api.delete(`/api/teachers/${id}/`)
  }
}