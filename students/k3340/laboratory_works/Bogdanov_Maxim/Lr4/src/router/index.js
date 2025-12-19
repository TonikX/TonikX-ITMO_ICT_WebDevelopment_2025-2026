import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const routes = [
  {
    path: '/',
    name: 'home',
    component: () => import('@/views/Home.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/login',
    name: 'login',
    component: () => import('@/views/Login.vue')
  },
  {
    path: '/register',
    name: 'register',
    component: () => import('@/views/Register.vue')
  },
  {
    path: '/teachers',
    name: 'teachers',
    component: () => import('@/views/Teachers.vue'),
    meta: { requiresAuth: true, requiresAdmin: true }
  },
  {
    path: '/students',
    name: 'students',
    component: () => import('@/views/Students.vue'),
    meta: { requiresAuth: true, requiresAdmin: true }
  },
  {
    path: '/classes',
    name: 'classes',
    component: () => import('@/views/Classes.vue'),
    meta: { requiresAuth: true, requiresAdmin: true }
  },
  {
    path: '/schedules',
    name: 'schedules',
    component: () => import('@/views/Schedules.vue'),
    meta: { requiresAuth: true, requiresAdmin: true }
  },
  {
    path: '/grades',
    name: 'grades',
    component: () => import('@/views/Grades.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/info',
    name: 'info',
    component: () => import('@/views/Info.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/reports',
    name: 'reports',
    component: () => import('@/views/Reports.vue'),
    meta: { requiresAuth: true }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()
  authStore.initAuth()

  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    next({ name: 'login' })
  } else if (to.meta.requiresAdmin && authStore.user?.role !== 'admin') {
    next({ name: 'home' })
  } else if ((to.name === 'login' || to.name === 'register') && authStore.isAuthenticated) {
    next({ name: 'home' })
  } else {
    next()
  }
})

export default router

