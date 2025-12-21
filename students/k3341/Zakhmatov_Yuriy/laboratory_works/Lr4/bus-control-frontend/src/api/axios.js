import axios from 'axios'

const apiClient = axios.create({
    baseURL: 'http://localhost:8000/api',
    withCredentials: false,
    headers: {
        Accept: 'application/json',
        'Content-Type': 'application/json'
    },
})

apiClient.interceptors.request.use(config => {
    const token = localStorage.getItem('access_token')
    if (token) {
        config.headers.Authorization = `Bearer ${token}`
    }
    return config
})

apiClient.interceptors.response.use(
    response => response,
    async error => {
        const originalRequest = error.config

        if (error.response?.status === 401 && !originalRequest._retry) {
            originalRequest._retry = true

            try {
                const refreshToken = localStorage.getItem('refresh_token')
                const response = await axios.post(
                    'http://localhost:8000/api/token/refresh/',
                    { refresh: refreshToken }
                )

                localStorage.setItem('access_token', response.data.access)
                originalRequest.headers.Authorization = `Bearer ${response.data.access}`

                return apiClient(originalRequest)
            } catch (refreshError) {
                // Если refresh не удался, разлогиниваем
                localStorage.removeItem('access_token')
                localStorage.removeItem('refresh_token')
                window.location.href = '/login'
                return Promise.reject(refreshError)
            }
        }

        return Promise.reject(error)
    }
)

export default apiClient
