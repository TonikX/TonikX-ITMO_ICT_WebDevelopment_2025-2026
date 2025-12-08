import './assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'
import apiClient from './api/client'
import { useAuthStore } from './stores/auth'

import 'vuetify/styles'
import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'

const vuetify = createVuetify({
  components,
  directives,
})

const app = createApp(App)

const pinia = createPinia()
app.use(pinia)
app.use(router)
app.use(vuetify)

app.config.globalProperties.$api = apiClient

const auth = useAuthStore(pinia)
if (auth.token && !auth.user) {
  auth.fetchUser()
}

app.mount('#app')
