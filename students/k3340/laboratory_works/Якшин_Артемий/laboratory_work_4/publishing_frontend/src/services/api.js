import axios from 'axios'

const API_BASE_URL = 'http://localhost:8000/api/v1'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Add auth token to requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('auth_token')
  if (token) {
    config.headers.Authorization = `Token ${token}`
  }
  return config
})

// Handle auth errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('auth_token')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

// Auth API
export const authApi = {
  login: (credentials) => api.post('/auth/token/login/', credentials),
  logout: () => api.post('/auth/token/logout/'),
  register: (userData) => api.post('/auth/users/', userData),
  getProfile: () => api.get('/auth/users/me/'),
  updateProfile: (data) => api.patch('/auth/users/me/', data),
  changePassword: (data) => api.post('/auth/users/set_password/', data),
}

// Employees API
export const employeesApi = {
  getAll: (params) => api.get('/employees/', { params }),
  getOne: (id) => api.get(`/employees/${id}/`),
  create: (data) => api.post('/employees/', data),
  update: (id, data) => api.put(`/employees/${id}/`, data),
  patch: (id, data) => api.patch(`/employees/${id}/`, data),
  delete: (id) => api.delete(`/employees/${id}/`),
}

// Authors API
export const authorsApi = {
  getAll: (params) => api.get('/authors/', { params }),
  getOne: (id) => api.get(`/authors/${id}/`),
  create: (data) => api.post('/authors/', data),
  update: (id, data) => api.put(`/authors/${id}/`, data),
  patch: (id, data) => api.patch(`/authors/${id}/`, data),
  delete: (id) => api.delete(`/authors/${id}/`),
}

// Books API
export const booksApi = {
  getAll: (params) => api.get('/books/', { params }),
  getOne: (id) => api.get(`/books/${id}/`),
  create: (data) => api.post('/books/', data),
  update: (id, data) => api.put(`/books/${id}/`, data),
  patch: (id, data) => api.patch(`/books/${id}/`, data),
  delete: (id) => api.delete(`/books/${id}/`),
}

// Contracts API
export const contractsApi = {
  getAll: (params) => api.get('/contracts/', { params }),
  getOne: (id) => api.get(`/contracts/${id}/`),
  create: (data) => api.post('/contracts/', data),
  update: (id, data) => api.put(`/contracts/${id}/`, data),
  patch: (id, data) => api.patch(`/contracts/${id}/`, data),
  delete: (id) => api.delete(`/contracts/${id}/`),
}

// Customers API
export const customersApi = {
  getAll: (params) => api.get('/customers/', { params }),
  getOne: (id) => api.get(`/customers/${id}/`),
  create: (data) => api.post('/customers/', data),
  update: (id, data) => api.put(`/customers/${id}/`, data),
  patch: (id, data) => api.patch(`/customers/${id}/`, data),
  delete: (id) => api.delete(`/customers/${id}/`),
}

// Orders API
export const ordersApi = {
  getAll: (params) => api.get('/orders/', { params }),
  getOne: (id) => api.get(`/orders/${id}/`),
  create: (data) => api.post('/orders/', data),
  update: (id, data) => api.put(`/orders/${id}/`, data),
  patch: (id, data) => api.patch(`/orders/${id}/`, data),
  delete: (id) => api.delete(`/orders/${id}/`),
}

// Book Authors API
export const bookAuthorsApi = {
  getAll: (params) => api.get('/book-authors/', { params }),
  create: (data) => api.post('/book-authors/', data),
  update: (id, data) => api.put(`/book-authors/${id}/`, data),
  delete: (id) => api.delete(`/book-authors/${id}/`),
}

// Book Editors API
export const bookEditorsApi = {
  getAll: (params) => api.get('/book-editors/', { params }),
  create: (data) => api.post('/book-editors/', data),
  update: (id, data) => api.put(`/book-editors/${id}/`, data),
  delete: (id) => api.delete(`/book-editors/${id}/`),
}

// Order Items API
export const orderItemsApi = {
  getAll: (params) => api.get('/order-items/', { params }),
  create: (data) => api.post('/order-items/', data),
  update: (id, data) => api.put(`/order-items/${id}/`, data),
  delete: (id) => api.delete(`/order-items/${id}/`),
}

// Reports API
export const reportsApi = {
  booksByAuthor: (authorId) => api.get('/reports/books-by-author/', { params: { author_id: authorId } }),
  chiefEditors: () => api.get('/reports/chief-editors/'),
  editorsPerBook: () => api.get('/reports/editors-per-book/'),
  contractsByMonth: (year) => api.get('/reports/contracts-by-month/', { params: { year } }),
  topManagers: (startDate, endDate) => api.get('/reports/top-managers/', { params: { start_date: startDate, end_date: endDate } }),
  quarterlyContracts: (quarter, year) => api.get('/reports/quarterly-contracts/', { params: { quarter, year } }),
}

export default api

