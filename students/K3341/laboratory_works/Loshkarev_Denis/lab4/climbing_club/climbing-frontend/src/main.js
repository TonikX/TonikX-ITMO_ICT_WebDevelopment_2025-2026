import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import vuetify from './plugins/vuetify' 

import './assets/main.css'

const app = createApp(App)

app.use(createPinia())
app.use(router)
app.use(vuetify) 

app.mount('#app')

window.addEventListener('error', (e) => console.error('Global error:', e.error || e.message))
window.addEventListener('unhandledrejection', (e) => console.error('Unhandled promise:', e.reason))