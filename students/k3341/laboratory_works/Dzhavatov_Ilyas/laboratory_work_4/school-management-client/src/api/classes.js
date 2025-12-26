import api from './auth'

export default {
  getClasses(params = {}) {
    return api.get('/api/school-classes/', { params })
  },

  getClass(id) {
    return api.get(`/api/school-classes/${id}/`)
  },

  createClass(data) {
    return api.post('/api/school-classes/', data)
  },

  updateClass(id, data) {
    return api.put(`/api/school-classes/${id}/`, data)
  },

  deleteClass(id) {
    return api.delete(`/api/school-classes/${id}/`)
  },

  getClassStudents(classId) {
    return api.get(`/api/school-classes/${classId}/students/`)
  }
}