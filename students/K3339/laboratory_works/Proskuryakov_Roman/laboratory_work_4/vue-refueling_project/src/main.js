import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import vuetify from './plugins/vuetify'

// Создаем приложение
const app = createApp(App)

// Используем Pinia
const pinia = createPinia()
app.use(pinia)

// Используем Router
app.use(router)

// Используем Vuetify
app.use(vuetify)

// Инициализируем авторизацию при запуске
import { useAuthStore } from './stores/auth'
const authStore = useAuthStore()
authStore.checkAuth()

// Монтируем приложение
app.mount('#app')