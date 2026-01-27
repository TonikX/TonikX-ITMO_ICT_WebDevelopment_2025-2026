import api from '../plugins/axios'

export const employeesApi = {
  getAll: (params) => api.get('/employees/', { params }),
  getById: (id) => api.get(`/employees/${id}/`),
  create: (data) => api.post('/employees/', data),
  update: (id, data) => api.patch(`/employees/${id}/`, data),
  delete: (id) => api.delete(`/employees/${id}/`),
  getStatistics: () => api.get('/employees/statistics/')
}

export const authorsApi = {
  getAll: (params) => api.get('/authors/', { params }),
  getById: (id) => api.get(`/authors/${id}/`),
  create: (data) => api.post('/authors/', data),
  update: (id, data) => api.patch(`/authors/${id}/`, data),
  delete: (id) => api.delete(`/authors/${id}/`),
  getBooks: (id) => api.get(`/authors/${id}/books/`)
}

export const booksApi = {
  getAll: (params) => api.get('/books/', { params }),
  getById: (id) => api.get(`/books/${id}/`),
  create: (data) => api.post('/books/', data),
  update: (id, data) => api.patch(`/books/${id}/`, data),
  delete: (id) => api.delete(`/books/${id}/`),
  getStatistics: () => api.get('/books/statistics/')
}

export const financialApi = {
  getAll: (params) => api.get('/financial/', { params }),
  getById: (id) => api.get(`/financial/${id}/`),
  create: (data) => api.post('/financial/', data),
  update: (id, data) => api.patch(`/financial/${id}/`, data),
  delete: (id) => api.delete(`/financial/${id}/`),
  getSummary: (params) => api.get('/financial/summary/', { params })
}

export const reportsApi = {
  getAll: (params) => api.get('/reports/', { params }),
  getById: (id) => api.get(`/reports/${id}/`),
  create: (data) => api.post('/reports/', data),
  update: (id, data) => api.patch(`/reports/${id}/`, data),
  delete: (id) => api.delete(`/reports/${id}/`)
}

