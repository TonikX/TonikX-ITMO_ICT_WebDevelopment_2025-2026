import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import vuetify from './plugins/vuetify'
import axios from 'axios'

// Настройка axios
axios.defaults.baseURL = 'http://localhost:8000'

// Интерцептор для добавления JWT токена
axios.interceptors.request.use(config => {
    const token = store.state.auth.token || localStorage.getItem('token')

    if (token) {
        config.headers.Authorization = `Bearer ${token}`
    }

    return config
}, error => {
    return Promise.reject(error)
})

// Интерцептор для обработки ответов
axios.interceptors.response.use(
    response => response,
    error => {
        if (error.response?.status === 401) {
            // Токен невалидный или просрочен
            store.commit('CLEAR_AUTH')
            localStorage.removeItem('token')
            localStorage.removeItem('user')

            if (router.currentRoute.value.path !== '/login') {
                router.push('/login')
            }
        }
        return Promise.reject(error)
    }
)

// Делаем axios глобально доступным
const app = createApp(App)
app.config.globalProperties.$axios = axios

app.use(store)
app.use(router)
app.use(vuetify)

app.mount('#app')