import api from './axios.js'

async function login(username, password) {
  const res = await api.post('/auth/token/login/', { username, password })
  const token = res.data.auth_token || res.data.token
  if (token) localStorage.setItem('token', token)
  return res.data
}

async function logout() {
  try {
    await api.post('/auth/token/logout/')
  } catch (e) {
  }
  localStorage.removeItem('token')
}

async function register(username, password, email = '') {
  return api.post('/auth/users/', { username, password, email })
}

async function getCurrentUser() {
  return api.get('/auth/users/me/')
}

async function updateUser(data) {
  return api.put('/auth/users/me/', data)
}

async function setPassword(current_password, new_password) {
  return api.post('/auth/users/set_password/', { current_password, new_password })
}

async function getBooks() {
  return api.get('/api/books/')
}

async function getBooksInHalls() {
  return api.get('/api/books-in-halls/')
}

async function getBookInHall(id) {
  return api.get(`/api/books-in-halls/${id}/`)
}

async function createBookInHall(data) {
  return api.post('/api/books-in-halls/', data)
}

async function updateBookInHall(id, data) {
  return api.put(`/api/books-in-halls/${id}/`, data)
}

async function deleteBookInHall(id) {
  return api.delete(`/api/books-in-halls/${id}/`)
}

async function getRareBooks() {
  return api.get('/api/books/rare/')
}

async function getHalls() {
  return api.get('/api/halls/')
}

async function getHall(id) {
  return api.get(`/api/halls/${id}/`)
}

async function createHall(data) {
  return api.post('/api/halls/', data)
}

async function updateHall(id, data) {
  return api.put(`/api/halls/${id}/`, data)
}

async function deleteHall(id) {
  return api.delete(`/api/halls/${id}/`)
}

async function getReaders() {
  return api.get('/api/readers/')
}

async function getReader(id) {
  return api.get(`/api/readers/${id}/`)
}

async function createReader(data) {
  return api.post('/api/readers/', data)
}

async function updateReader(id, data) {
  return api.put(`/api/readers/${id}/`, data)
}

async function deleteReader(id) {
  return api.delete(`/api/readers/${id}/`)
}

async function getIssues() {
  return api.get('/api/issues/')
}

async function getIssue(id) {
  return api.get(`/api/issues/${id}/`)
}

async function createIssue(data) {
  return api.post('/api/issues/', data)
}

async function updateIssue(id, data) {
  return api.put(`/api/issues/${id}/`, data)
}

async function deleteIssue(id) {
  return api.delete(`/api/issues/${id}/`)
}

async function getReaderBooks(readerId) {
  return api.get(`/api/readers/${readerId}/books/`)
}

async function getIssuesOverdue() {
  return api.get('/api/issues/overdue/')
}

async function getReadersUnder20() {
  return api.get('/api/readers/under_20/')
}

async function getEducationStats() {
  return api.get('/api/readers/education_stats/')
}

async function getRareBooksReaders() {
  return api.get('/api/readers/rare_books/')
}

async function getBook(id) {
  return api.get(`/api/books/${id}/`)
}

async function createBook(data) {
  return api.post('/api/books/', data)
}

async function updateBook(id, data) {
  return api.put(`/api/books/${id}/`, data)
}

async function deleteBook(id) {
  return api.delete(`/api/books/${id}/`)
}

export default {
  login,
  logout,
  register,
  getCurrentUser,
  updateUser,
  setPassword,
  getBooks,
  getBooksInHalls,
  getBookInHall,
  createBookInHall,
  updateBookInHall,
  deleteBookInHall,
  getRareBooks,
  getHalls,
  getReaders,
  getIssues,
  getBook,
  createBook,
  updateBook,
  deleteBook,
  getHall,
  createHall,
  updateHall,
  deleteHall,
  getReader,
  createReader,
  updateReader,
  deleteReader,
  getIssue,
  createIssue,
  updateIssue,
  deleteIssue,
  getReaderBooks,
  getIssuesOverdue,
  getReadersUnder20,
  getEducationStats,
  getRareBooksReaders,
}
