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
      meta: { requiresGuest: true },
    },
    {
      path: '/register',
      name: 'register',
      component: () => import('@/views/RegisterView.vue'),
      meta: { requiresGuest: true },
    },
    {
      path: '/profile',
      name: 'profile',
      component: () => import('@/views/ProfileView.vue'),
      meta: { requiresAuth: true },
    },
    {
      path: '/settings',
      name: 'settings',
      component: () => import('@/views/SettingsView.vue'),
      meta: { requiresAuth: true },
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

// Гварды маршрутов
router.beforeEach(async (to, from, next) => {
  const authStore = useAuthStore()

  // Если маршрут требует аутентификации
  if (to.meta.requiresAuth) {
    if (!authStore.isAuthenticated) {
      // Пытаемся восстановить сессию из localStorage
      if (authStore.accessToken && authStore.refreshToken) {
        try {
          await authStore.loadUser()
          await authStore.loadProfile()
          if (authStore.isAuthenticated) {
            next()
            return
          }
        } catch (error) {
          // Не удалось восстановить - редирект на логин
          authStore.logout()
        }
      }
      next({ name: 'login', query: { redirect: to.fullPath } })
      return
    }
    next()
    return
  }

  // Если маршрут доступен только для гостей (неавторизованных)
  if (to.meta.requiresGuest) {
    if (authStore.isAuthenticated) {
      next({ name: 'profile' })
      return
    }
    next()
    return
  }

  next()
})

export default router
