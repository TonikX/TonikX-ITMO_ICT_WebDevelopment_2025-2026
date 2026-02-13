import axios from 'axios';

const API_URL = 'http://localhost:8000/';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

const authAPI = {
  register(data) {
    return api.post('auth/users/', data);
  },

  login(data) {
    return api.post('auth/token/login/', data);
  },

  logout() {
    return api.post('auth/token/logout/')
  },

  getBooks() {
    return api.get('books/', {headers: {Authorization: `Token ${localStorage.getItem('auth_token')}`}});
  },

  createBook(data) {
    return api.post('books/', data, {
      headers: {Authorization: `Token ${localStorage.getItem('auth_token')}`}});
  },

  updateBook(id, data) {
    return api.patch(`books/${id}/`, data, {headers: {Authorization: `Token ${localStorage.getItem('auth_token')}`}});
  },

  deleteBook(id) {
    return api.delete(`books/${id}/`, {headers: {Authorization: `Token ${localStorage.getItem('auth_token')}`}});
  },

  getReaders() {
    return api.get('readers/', {headers: {Authorization: `Token ${localStorage.getItem('auth_token')}`}});
  },

  createReader(data) {
    return api.post('readers/', data, {headers: {Authorization: `Token ${localStorage.getItem('auth_token')}`}});
  },

  updateReader(id, data) {
    return api.patch(`readers/${id}/`, data, {headers: {Authorization: `Token ${localStorage.getItem('auth_token')}`}});
  },

  deleteReader(id) {
    return api.delete(`readers/${id}/`, {headers: {Authorization: `Token ${localStorage.getItem('auth_token')}`}});
  },

  getHalls() {
    return api.get('halls/', {headers: {Authorization: `Token ${localStorage.getItem('auth_token')}`}});
  },

  createHall(data) {
    return api.post('halls/', data, {headers: {Authorization: `Token ${localStorage.getItem('auth_token')}`}});
  },

  updateHall(id, data) {
    return api.patch(`halls/${id}/`, data, {headers: {Authorization: `Token ${localStorage.getItem('auth_token')}`}});
  },

  deleteHall(id) {
    return api.delete(`halls/${id}/`, {headers: {Authorization: `Token ${localStorage.getItem('auth_token')}`}});
  },

  getReadings() {
    return api.get('readings/', {headers: {Authorization: `Token ${localStorage.getItem('auth_token')}`}});
  },

  createReading(data) {
    return api.post('readings/', data, {headers: {Authorization: `Token ${localStorage.getItem('auth_token')}`}});
  },

  updateReading(id, data) {
    return api.patch(`readings/${id}/`, data, {headers: {Authorization: `Token ${localStorage.getItem('auth_token')}`}});
  },

  deleteReading(id) {
    return api.delete(`readings/${id}/`, {headers: {Authorization: `Token ${localStorage.getItem('auth_token')}`}});
  },

  getEducationStats() {
    return api.get('readers/stats/education/', {headers: {Authorization: `Token ${localStorage.getItem('auth_token')}`}});
  },

  getYoungReadersCount() {
    return api.get('readers/stats/young/', {headers: {Authorization: `Token ${localStorage.getItem('auth_token')}`}});
  },

  getReaderBooks(id) {
    return api.get(`readers/${id}/books/`, {headers: { Authorization: `Token ${localStorage.getItem('auth_token')}`}});
  },

  getBadReaders() {
    return api.get('readers/bad/', {headers: {Authorization: `Token ${localStorage.getItem('auth_token')}`}});
  },

  getRareBookReaders() {
    return api.get('readers/rare-books/', {headers: {Authorization: `Token ${localStorage.getItem('auth_token')}`}});
  },

  getMonthlyReport(year, month) {
    return api.get(`reports/monthly/${year}/${month}/`, {headers: { Authorization: `Token ${localStorage.getItem('auth_token')}`}});
  }
};

export default authAPI;