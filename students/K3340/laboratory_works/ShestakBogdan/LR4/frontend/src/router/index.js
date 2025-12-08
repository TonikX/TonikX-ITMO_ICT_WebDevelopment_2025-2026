// src/router/index.js
import { createRouter, createWebHistory } from 'vue-router'
import LoginView from '../views/auth/LoginView.vue'
import RegisterView from '../views/auth/RegisterView.vue'
import ProfileView from '../views/auth/ProfileView.vue'
import DriversView from '../views/DriversView.vue'
import ShiftsView from '../views/ShiftsView.vue'

const routes = [
  { path: '/', redirect: '/drivers' },

  { path: '/login', name: 'Login', component: LoginView, meta: { public: true } },
  { path: '/register', name: 'Register', component: RegisterView, meta: { public: true } },

  { path: '/profile', name: 'Profile', component: ProfileView },
  { path: '/drivers', name: 'Drivers', component: DriversView },
  { path: '/shifts', name: 'Shifts', component: ShiftsView },
  // сюда потом добавишь /buses, /routes, /shifts, /report
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach((to, from, next) => {
  const isPublic = to.meta.public
  const token = localStorage.getItem('auth_token')

  if (!isPublic && !token) {
    return next('/login')
  }
  next()
})

export default router