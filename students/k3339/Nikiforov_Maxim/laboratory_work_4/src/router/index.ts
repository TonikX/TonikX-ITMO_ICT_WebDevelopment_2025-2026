import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/login',
      name: 'login',
      component: () => import('../pages/LoginPage.vue'),
      meta: { guest: true },
    },
    {
      path: '/register',
      name: 'register',
      component: () => import('../pages/RegisterPage.vue'),
      meta: { guest: true },
    },
    {
      path: '/',
      component: () => import('../layouts/MainLayout.vue'),
      meta: { requiresAuth: true },
      children: [
        { path: '', name: 'home', component: () => import('../pages/HomePage.vue') },
        { path: 'profile', name: 'profile', component: () => import('../pages/ProfilePage.vue') },
        { path: 'reading-rooms', name: 'reading-rooms', component: () => import('../pages/ReadingRoomsPage.vue') },
        { path: 'readers', name: 'readers', component: () => import('../pages/ReadersPage.vue') },
        { path: 'books', name: 'books', component: () => import('../pages/BooksPage.vue') },
        { path: 'assignments', name: 'assignments', component: () => import('../pages/AssignmentsPage.vue') },
        { path: 'librarian', name: 'librarian', component: () => import('../pages/LibrarianPage.vue') },
        { path: 'queries', name: 'queries', component: () => import('../pages/QueriesPage.vue') },
      ],
    },
  ],
})

router.beforeEach(async (to, _from, next) => {
  const auth = useAuthStore()
  if (auth.token && !auth.user) {
    await auth.initUser()
  }
  if (to.meta.requiresAuth && !auth.isAuthenticated) {
    next({ name: 'login', query: { redirect: to.fullPath } })
  } else if (to.meta.guest && auth.isAuthenticated) {
    next({ name: 'home' })
  } else {
    next()
  }
})

export default router
