import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/authStore'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      name: 'home',
      component: () => import('@/views/HomeView.vue'),
      meta: { requiresAuth: true },
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('@/views/LoginView.vue'),
    },
    {
      path: '/register',
      name: 'register',
      component: () => import('@/views/RegisterView.vue'),
    },
    {
      path: '/drones',
      name: 'drones',
      component: () => import('@/views/DronesView.vue'),
      meta: { requiresAuth: true },
    },
    {
      path: '/drones/:id',
      name: 'drone-detail',
      component: () => import('@/views/DroneDetailView.vue'),
      meta: { requiresAuth: true },
    },
    {
      path: '/flights',
      name: 'flights',
      component: () => import('@/views/FlightsView.vue'),
      meta: { requiresAuth: true },
    },
    {
      path: '/flights/:id',
      name: 'flight-detail',
      component: () => import('@/views/FlightDetailView.vue'),
      meta: { requiresAuth: true },
    },
  ],
})

router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()

  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    next({ name: 'login' })
    return
  }

  // Если уже авторизован и идёт на login/register — редирект на главную
  if ((to.name === 'login' || to.name === 'register') && authStore.isAuthenticated) {
    next({ name: 'home' })
    return
  }

  next()
})

export default router
