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
    return api.get(`/api/students/${studentId}/grades/`)
  },

  updateStudentGrade(studentId, gradeId, data) {
    return api.put(`/api/students/${studentId}/grades/${gradeId}/`, data)
  }
}