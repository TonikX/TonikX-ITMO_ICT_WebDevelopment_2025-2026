import api from './auth'

const normalizeClass = item => ({
  ...item,
  class_name: item.name ?? item.class_name,
  students_count: item.student_count ?? item.students_count ?? 0
})

const normalizeResponse = response => {
  const data = response.data
  if (Array.isArray(data)) {
    response.data = data.map(normalizeClass)
    return response
  }
  if (data?.results) {
    response.data = { ...data, results: data.results.map(normalizeClass) }
  }
  return response
}

export default {
  getClasses(params = {}) {
    return api.get('/api/schoolclasses/', { params }).then(normalizeResponse)
  },

  getClass(id) {
    return api.get(`/api/schoolclasses/${id}/`).then(normalizeResponse)
  },

  createClass(data) {
    return api.post('/api/schoolclasses/', data)
  },

  updateClass(id, data) {
    return api.put(`/api/schoolclasses/${id}/`, data)
  },

  deleteClass(id) {
    return api.delete(`/api/schoolclasses/${id}/`)
  }
}