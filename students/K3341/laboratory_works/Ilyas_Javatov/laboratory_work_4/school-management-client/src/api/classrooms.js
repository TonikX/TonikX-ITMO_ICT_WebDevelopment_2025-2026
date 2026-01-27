import api from './auth'

export default {
  getClassrooms(params = {}) {
    return api.get('/api/classrooms/', { params })
  },

  getClassroom(id) {
    return api.get(`/api/classrooms/${id}/`)
  },

  createClassroom(data) {
    return api.post('/api/classrooms/', data)
  },

  updateClassroom(id, data) {
    return api.put(`/api/classrooms/${id}/`, data)
  },

  deleteClassroom(id) {
    return api.delete(`/api/classrooms/${id}/`)
  }
}