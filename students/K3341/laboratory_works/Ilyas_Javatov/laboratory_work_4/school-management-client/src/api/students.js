import api from './auth'

export default {
  getStudents(params = {}) {
    return api.get('/api/students/', { params })
  },

  getStudent(id) {
    return api.get(`/api/students/${id}/`)
  },

  createStudent(data) {
    return api.post('/api/students/', data)
  },

  updateStudent(id, data) {
    return api.put(`/api/students/${id}/`, data)
  },

  deleteStudent(id) {
    return api.delete(`/api/students/${id}/`)
  },

  getStudentGrades(studentId) {
    return api.get('/api/grades/').then(response => {
      const data = Array.isArray(response.data) ? response.data : response.data.results || []
      response.data = data.filter(item => item.student === studentId)
      return response
    })
  },

  updateStudentGrade(studentId, gradeId, data) {
    return api.put(`/api/grades/${gradeId}/`, data)
  }
}