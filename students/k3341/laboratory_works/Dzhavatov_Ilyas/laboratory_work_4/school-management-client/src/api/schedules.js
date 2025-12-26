import api from './auth'

export default {
  getSchedules(params = {}) {
    return api.get('/api/schedules/', { params })
  },

  getSchedule(id) {
    return api.get(`/api/schedules/${id}/`)
  },

  createSchedule(data) {
    return api.post('/api/schedules/', data)
  },

  updateSchedule(id, data) {
    return api.put(`/api/schedules/${id}/`, data)
  },

  deleteSchedule(id) {
    return api.delete(`/api/schedules/${id}/`)
  },

  getLesson(params) {
    return api.get('/api/schedules/get_lesson/', { params })
  }
}