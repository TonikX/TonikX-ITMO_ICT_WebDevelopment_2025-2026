// src/api/config.js
import axios from 'axios'

const API_BASE = 'http://localhost:8000/api'
const AUTH_BASE = 'http://localhost:8000/auth'

// Глобальная настройка axios
axios.defaults.baseURL = API_BASE
axios.interceptors.request.use(config => {
  const token = localStorage.getItem('authToken')
  if (token) config.headers.Authorization = `Token ${token}`
  return config
})

export { API_BASE, AUTH_BASE, axios }