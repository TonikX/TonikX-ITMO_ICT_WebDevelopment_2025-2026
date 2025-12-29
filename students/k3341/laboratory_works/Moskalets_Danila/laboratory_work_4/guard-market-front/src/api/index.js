import axios from 'axios'
import router from '@/router'

const apiClient = axios.create({
    baseURL: 'http://127.0.0.1:8000/api/v1/',
    headers: {
        'Content-Type': 'application/json',
    },
    timeout: 10000 // 10 секунд таймаут
})

// Перехватчик для добавления токена
apiClient.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem('access_token')
        if (token) {
            config.headers.Authorization = `Bearer ${token}`
        }
        return config
    },
    (error) => {
        return Promise.reject(error)
    }
)

// Перехватчик для обновления токена при истечении
apiClient.interceptors.response.use(
    (response) => response,
    async (error) => {
        const originalRequest = error.config

        // Если ошибка 401 и это не запрос на обновление токена
        if (error.response?.status === 401 &&
            !originalRequest._retry &&
            !originalRequest.url.includes('auth/jwt/refresh/') &&
            originalRequest.url !== 'auth/jwt/create/') {

            const refreshToken = localStorage.getItem('refresh_token')

            // Проверяем наличие refresh токена
            if (!refreshToken) {
                // Если нет refresh токена, просто разлогиниваем
                localStorage.removeItem('access_token')
                localStorage.removeItem('user')

                if (router.currentRoute.value.path !== '/login') {
                    router.push('/login')
                }
                return Promise.reject(error)
            }

            originalRequest._retry = true

            try {
                const response = await axios.post(
                    'http://127.0.0.1:8000/api/v1/auth/jwt/refresh/',
                    { refresh: refreshToken },
                    { timeout: 5000 }
                )

                localStorage.setItem('access_token', response.data.access)
                apiClient.defaults.headers.common['Authorization'] = `Bearer ${response.data.access}`

                return apiClient(originalRequest)
            } catch (refreshError) {
                // Если обновление токена не удалось, разлогиниваем
                localStorage.removeItem('access_token')
                localStorage.removeItem('refresh_token')
                localStorage.removeItem('user')

                if (router.currentRoute.value.path !== '/login') {
                    router.push('/login')
                }
                return Promise.reject(refreshError)
            }
        }

        return Promise.reject(error)
    }
)

export default apiClient