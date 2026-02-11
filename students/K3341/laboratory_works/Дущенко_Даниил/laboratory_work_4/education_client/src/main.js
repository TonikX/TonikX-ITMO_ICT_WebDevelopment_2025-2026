import { createApp } from 'vue'
import App from './App.vue'
import { createRouter, createWebHistory } from 'vue-router'


import 'vuetify/styles'
import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'
import '@mdi/font/css/materialdesignicons.css'


import Login from './components/Login.vue'
import Assignments from './components/Assignments.vue'
import Submission from './components/Submission.vue'
import Reviews from './components/Reviews.vue'
import TeacherDashboard from './components/TeacherDashboard.vue'
import Register from './components/Register.vue'
import Profile from './components/Profile.vue'

const eduDarkTheme = {
  dark: true,
  colors: {
    background: '#121212',
    surface: '#1E1E1E',
    primary: '#10B981',    
    secondary: '#3B82F6',
    error: '#EF4444',
  }
}

const vuetify = createVuetify({
  components,
  directives,
  theme: {
    defaultTheme: 'eduDarkTheme',
    themes: { eduDarkTheme },
  },
  defaults: {
    VCard: { rounded: 'lg', elevation: 2 },
    VBtn: { rounded: 'lg', height: 44, fontWeight: '600' },
    VTextField: { variant: 'outlined', density: 'comfortable', color: 'primary' },
    VTextarea: { variant: 'outlined', density: 'comfortable', color: 'primary' },
    VSelect: { variant: 'outlined', density: 'comfortable', color: 'primary' },
  }
})

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', component: Login },
    { path: '/register', component: Register },
    { path: '/profile', component: Profile }, 
    { path: '/assignments', component: Assignments },
    { path: '/submit', component: Submission },
    { path: '/reviews', component: Reviews },
    { path: '/dashboard', component: TeacherDashboard },
  ]
})

createApp(App).use(vuetify).use(router).mount('#app')