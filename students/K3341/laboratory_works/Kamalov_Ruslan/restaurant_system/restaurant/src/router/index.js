import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'Dashboard',
      component: () => import('@/views/Dashboard.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/login',
      name: 'Login',
      component: () => import('@/views/Login.vue')
    },
    {
      path: '/register',
      name: 'Register',
      component: () => import('@/views/Register.vue')
    },
    {
      path: '/employees',
      name: 'Employees',
      component: () => import('@/views/Employees.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/ingredients',
      name: 'Ingredients',
      component: () => import('@/views/Ingredients.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/dishes',
      name: 'Dishes',
      component: () => import('@/views/Dishes.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/tables',
      name: 'Tables',
      component: () => import('@/views/Tables.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/orders',
      name: 'Orders',
      component: () => import('@/views/Orders.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/positions',
      name: 'Positions',
      component: () => import('@/views/Positions.vue'),
      meta: { requiresAuth: true }
    }
  ],
})

router.beforeEach((to, from, next) => {
  const { isAuthenticated } = useAuthStore()
  
  if (to.meta.requiresAuth && !isAuthenticated.value) {
    next('/login')
  } else if ((to.name === 'Login' || to.name === 'Register') && isAuthenticated.value) {
    next('/')
  } else {
    next()
  }
})

export default router
