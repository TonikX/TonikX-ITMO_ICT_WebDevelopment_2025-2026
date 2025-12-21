import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const routes = [
  { path: '/', redirect: '/login' },
  { path: '/login', name: 'login', component: () => import('../views/LoginView.vue') },
  { path: '/register', name: 'register', component: () => import('../views/RegisterView.vue') },
  { path: '/profile', name: 'profile', component: () => import('../views/ProfileView.vue'), meta: { requiresAuth: true } },
  { path: '/dashboard', name: 'dashboard', component: () => import('../views/DashboardView.vue'), meta: { requiresAuth: true } },
  { path: '/subjects', name: 'subjects', component: () => import('../views/SubjectsView.vue'), meta: { requiresAuth: true } },
  { path: '/classes', name: 'classes', component: () => import('../views/ClassesView.vue'), meta: { requiresAuth: true } },
  { path: '/classrooms', name: 'classrooms', component: () => import('../views/ClassroomsView.vue'), meta: { requiresAuth: true } },
  { path: '/teachers', name: 'teachers', component: () => import('../views/TeachersView.vue'), meta: { requiresAuth: true } },
  { path: '/students', name: 'students', component: () => import('../views/StudentsView.vue'), meta: { requiresAuth: true } },
  { path: '/schedule', name: 'schedule', component: () => import('../views/ScheduleView.vue'), meta: { requiresAuth: true } },
  { path: '/grades', name: 'grades', component: () => import('../views/GradesView.vue'), meta: { requiresAuth: true } },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach((to, from, next) => {
  const auth = useAuthStore()
  if (to.meta.requiresAuth && !auth.isAuthenticated) {
    next({ name: 'login', query: { next: to.fullPath } })
  } else if ((to.name === 'login' || to.name === 'register') && auth.isAuthenticated) {
    next({ name: 'dashboard' })
  } else {
    next()
  }
})

export default router

