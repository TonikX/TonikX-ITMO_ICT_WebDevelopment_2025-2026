import axios from "axios"

const api = axios.create({
  baseURL: "http://127.0.0.1:8000",
  headers: {
    'Content-Type': 'application/json',
  }
})

api.interceptors.request.use(config => {
  const publicAuthEndpoints = [
    '/auth/token/login/',
    '/auth/users/',
    '/auth/token/logout/',
  ]
  
  const isPublicEndpoint = publicAuthEndpoints.some(endpoint => config.url === endpoint)
  
  if (!isPublicEndpoint) {
    const token = localStorage.getItem("token")
    if (token) {
      config.headers.Authorization = `Token ${token}`
    }
  }
  
  return config
})

api.interceptors.response.use(
  response => response,
  error => {
    console.error('API Error:', error.response?.status, error.response?.data || error.message)
    return Promise.reject(error)
  }
)

export default api