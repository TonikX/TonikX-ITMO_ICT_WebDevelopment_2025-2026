import api from './auth'

const normalizeSubject = subject => ({
  ...subject,
  subject_name: subject.name ?? subject.subject_name
})

const normalizeResponse = response => {
  const data = response.data
  if (Array.isArray(data)) {
    response.data = data.map(normalizeSubject)
    return response
  }
  if (data?.results) {
    response.data = { ...data, results: data.results.map(normalizeSubject) }
  }
  return response
}

export default {
  getSubjects(params = {}) {
    return api.get('/api/subjects/', { params }).then(normalizeResponse)
  },

  getSubject(id) {
    return api.get(`/api/subjects/${id}/`).then(normalizeResponse)
  },

  createSubject(data) {
    return api.post('/api/subjects/', data)
  },

  updateSubject(id, data) {
    return api.put(`/api/subjects/${id}/`, data)
  },

  deleteSubject(id) {
    return api.delete(`/api/subjects/${id}/`)
  }
}
