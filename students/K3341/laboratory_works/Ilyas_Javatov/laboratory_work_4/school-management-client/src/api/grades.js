import api from './auth'

export default {
  getGrades(params = {}) {
    return api.get('/api/grades/', { params })
  },

  getGrade(id) {
    return api.get(`/api/grades/${id}/`)
  },

  createGrade(data) {
    return api.post('/api/grades/', data)
  },

  updateGrade(id, data) {
    return api.put(`/api/grades/${id}/`, data)
  },

  deleteGrade(id) {
    return api.delete(`/api/grades/${id}/`)
  },

  getStudentGrades(studentId) {
    return api.get('/api/grades/').then(response => {
      const data = Array.isArray(response.data) ? response.data : response.data.results || []
      response.data = data.filter(item => item.student === studentId)
      return response
    })
  }
}