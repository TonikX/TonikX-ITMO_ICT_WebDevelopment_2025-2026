import { createApp } from 'vue'
import { createPinia } from 'pinia'
import { createRouter } from './router'
import App from './App.vue'
import { vuetify } from './plugins/vuetify'
import { useAuthStore } from './stores/auth'

const app = createApp(App)

const pinia = createPinia()
app.use(pinia)

const auth = useAuthStore(pinia)
auth.hydrate()

const router = createRouter()
app.use(router)

app.use(vuetify)
app.mount('#app')
