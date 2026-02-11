import './assets/main.css'
import './assets/global.css'
import { createApp } from 'vue'
import { createPinia } from 'pinia'

// Vuetify
import 'vuetify/styles'
import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'
import { aliases, mdi } from 'vuetify/iconsets/mdi'

import App from './App.vue'
import router from './router'
import apiClient from './api/client'
import { useAuthStore } from './stores/auth'

// Создаем Vuetify
const vuetify = createVuetify({
  components,
  directives,
  icons: {
    defaultSet: 'mdi',
    aliases,
    sets: {
      mdi,
    },
  },
  theme: {
    defaultTheme: 'light',
  },
})

const app = createApp(App)

const pinia = createPinia()
app.use(pinia)
app.use(router)
app.use(vuetify)

app.config.globalProperties.$api = apiClient

const auth = useAuthStore()
if (auth.token && !auth.user) {
  auth.fetchUser()
}

app.mount('#app')