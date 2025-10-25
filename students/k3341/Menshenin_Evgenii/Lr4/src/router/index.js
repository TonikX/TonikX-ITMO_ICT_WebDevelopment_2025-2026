import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/login',
      name: 'login',
      component: () => import('@/views/Login.vue'),
      meta: { requiresGuest: true }
    },
    {
      path: '/register',
      name: 'register',
      component: () => import('@/views/Register.vue'),
      meta: { requiresGuest: true }
    },
    {
      path: '/',
      name: 'dashboard',
      component: () => import('@/views/Dashboard.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/profile',
      name: 'profile',
      component: () => import('@/views/Profile.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/fleet',
      name: 'fleet',
      component: () => import('@/views/Fleet.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/flights',
      name: 'flights',
      component: () => import('@/views/Flights.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/flights/:id',
      name: 'flight-details',
      component: () => import('@/views/FlightDetails.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/employees',
      name: 'employees',
      component: () => import('@/views/Employees.vue'),
      meta: { requiresAuth: true }
    }
  ]
})

// Navigation guard
router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()
  
  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    next('/login')
  } else if (to.meta.requiresGuest && authStore.isAuthenticated) {
    next('/')
  } else {
    next()
  }
})

export default router