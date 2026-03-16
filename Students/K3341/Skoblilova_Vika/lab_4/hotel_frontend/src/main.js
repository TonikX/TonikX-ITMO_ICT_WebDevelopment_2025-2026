import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import vuetify from './plugins/vuetify'
import axios from 'axios'

// Настройка базового URL для API (адрес вашего Django-сервера)
axios.defaults.baseURL = 'http://127.0.0.1:8000/api/'

// Добавляем интерцептор для авторизации
axios.interceptors.request.use(
  config => {
    const token = localStorage.getItem('auth_token')
    if (token) {
      config.headers.Authorization = `Token ${token}`
    }
    return config
  },
  error => Promise.reject(error)
)

const app = createApp(App)
app.use(router)
app.use(vuetify)
app.config.globalProperties.$axios = axios
app.mount('#app')