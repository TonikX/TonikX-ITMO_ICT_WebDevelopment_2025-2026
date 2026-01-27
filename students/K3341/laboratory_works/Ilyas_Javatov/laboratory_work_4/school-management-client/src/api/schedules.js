import api from './auth'

export default {
  getSchedules(params = {}) {
    return api.get('/api/schedule/', { params })
  },

  getSchedule(id) {
    return api.get(`/api/schedule/${id}/`)
  },

  createSchedule(data) {
    const { classroom, ...payload } = data
    return api.post('/api/schedule/', payload)
  },

  updateSchedule(id, data) {
    const { classroom, ...payload } = data
    return api.put(`/api/schedule/${id}/`, payload)
  },

  deleteSchedule(id) {
    return api.delete(`/api/schedule/${id}/`)
  },

  getLesson(params) {
    const mappedParams = {
      class_id: params.class_id,
      day: params.day_of_week,
      lesson: params.lesson_number
    }
    return api.get('/api/reports/subject_for_class/', { params: mappedParams })
  }
}