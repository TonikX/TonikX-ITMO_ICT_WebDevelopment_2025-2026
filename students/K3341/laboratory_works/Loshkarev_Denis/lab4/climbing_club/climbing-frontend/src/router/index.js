import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../stores/auth' 

import LoginView from '../views/LoginView.vue'
import MountainsView from '../views/MountainsView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/login',
      name: 'login',
      component: LoginView,
      meta: { requiresAuth: false } 
    },
    {
      path: '/',
      redirect: '/mountains'
    },
    {
      path: '/mountains',
      name: 'mountains',
      component: MountainsView,
      meta: { requiresAuth: true } 
    }
  ]
})

// Навигационный страж (Global Before Guard)
router.beforeEach((to, from, next) => {
  const auth = useAuthStore()

  if (to.meta.requiresAuth && !auth.token) {
    next('/login')
  } 
  else if (to.name === 'login' && auth.token) {
    next('/mountains')
  } 
  else {
    next()
  }
})

export default router
