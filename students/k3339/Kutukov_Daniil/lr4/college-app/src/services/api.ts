import axios from 'axios'

const api = axios.create({
    baseURL: 'http://127.0.0.1:8003/api',
    headers: {
        'Content-Type': 'application/json',
    },
})

// Добавляем токен к каждому запросу
api.interceptors.request.use((config) => {
    const token = localStorage.getItem('auth_token')
    if (token) {
        config.headers.Authorization = `Token ${token}`
    }
    return config
})

// Обработка ошибок
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

export default api
