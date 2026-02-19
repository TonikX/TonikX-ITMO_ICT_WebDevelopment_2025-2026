import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import vuetify from './plugins/vuetify'
import axios from 'axios'

import { API_BASE } from './api/endpoints'

// настройка axios
axios.defaults.baseURL = 'http://localhost:8000/api/'

// Интерцептор для добавления JWT токена ко всем запросам
axios.interceptors.request.use(config => {
    // Логируем запрос (можно убрать в продакшене)
    console.log(`[AXIOS REQUEST] ${config.method.toUpperCase()} ${config.url}`, {
        data: config.data,
        headers: config.headers
    })

    // Получаем токен из localStorage
    const token = localStorage.getItem('token')

    // Если токен есть - добавляем в заголовки
    if (token) {
        config.headers.Authorization = `Bearer ${token}`
        console.log(`[AXIOS] Добавлен токен в заголовок: Bearer ${token.substring(0, 20)}...`)
    } else {
        console.log('[AXIOS] Токен не найден, запрос без авторизации')
    }

    return config
}, error => {
    console.error('[AXIOS REQUEST ERROR]', error)
    return Promise.reject(error)
})

// Интерцептор для обработки ответов
axios.interceptors.response.use(
    response => {
        console.log(`[AXIOS RESPONSE] ${response.status} ${response.config.url}`, {
            data: response.data
        })
        return response
    },
    error => {
        const { config, response } = error

        console.error('[AXIOS RESPONSE ERROR]', {
            url: config?.url,
            method: config?.method,
            status: response?.status,
            data: response?.data,
            message: error.message
        })

        // Если 401 Unauthorized - удаляем токен и перенаправляем на логин
        if (response?.status === 401) {
            console.log('[AXIOS] 401 ошибка, очищаем токен')
            localStorage.removeItem('token')

            // Диспатчим logout в store если приложение уже инициализировано
            if (store && store.state?.auth) {
                store.commit('auth/LOGOUT')
            }

            // Перенаправляем на страницу логина если не на ней
            if (router && !window.location.pathname.includes('/login')) {
                router.push('/login')
            }
        }

        return Promise.reject(error)
    }
)


const app = createApp(App)

// Делаем axios доступным глобально в компонентах через this.$axios
app.config.globalProperties.$axios = axios

// Подключаем плагины
app.use(router)
app.use(store)
app.use(vuetify)

// Монтируем приложение
app.mount('#app')

// Экспортируем axios для использования в других модулях
export default axios