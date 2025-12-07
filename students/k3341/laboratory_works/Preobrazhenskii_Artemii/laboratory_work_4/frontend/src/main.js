import { createPinia } from 'pinia'
import { createApp } from 'vue'
import { createRouter, createWebHistory } from 'vue-router'

import App from './App.vue'
import routes from './router'
import './styles.scss'

import '@mdi/font/css/materialdesignicons.css'
import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'
import 'vuetify/styles'
import { useAuthStore } from './stores/auth'
import api from './utils/api'

const vuetify = createVuetify({
  components,
  directives
})

const app = createApp(App)
const pinia = createPinia()
const router = createRouter({ history: createWebHistory(), routes })

app.use(pinia)
app.use(router)
app.use(vuetify)

// Initialize API auth header from stored token (if any)
api.setAuth(localStorage.getItem('token') || null)

// Fetch current user if token exists
const auth = useAuthStore()
if (auth.token) {
  // fire-and-forget; store will populate user
  auth.fetchMe().catch(() => { /* ignore */ })
}

// Simple navigation guard for routes that require authentication
router.beforeEach((to, from, next) => {
  const requires = to.meta && to.meta.requiresAuth
  if (requires && !auth.isAuthenticated) return next({ name: 'login' })
  if ((to.name === 'login' || to.name === 'register') && auth.isAuthenticated) return next({ name: 'files' })
  return next()
})

app.mount('#app')