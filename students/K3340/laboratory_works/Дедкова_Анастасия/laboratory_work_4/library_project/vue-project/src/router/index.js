import { createRouter, createWebHistory } from 'vue-router'

import BooksView from '@/views/BooksView.vue'
import LoginView from '@/views/LoginView.vue'
import RegisterView from '@/views/RegisterView.vue'
import ProfileView from '@/views/ProfileView.vue'
import OnLoanView from '@/views/OnLoanView.vue'
import ManageLoansView from '@/views/ManageLoansView.vue'
import ReportsView from '@/views/ReportsView.vue'
import CopiesManageView from '@/views/CopiesManageView.vue'

import { useAuthStore } from '@/stores/auth'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: '/', redirect: '/books' },

    {
      path: '/books',
      name: 'books',
      component: BooksView,
    },
    {
      path: '/login',
      name: 'login',
      component: LoginView,
      meta: { guestOnly: true },
    },
    {
      path: '/register',
      name: 'register',
      component: RegisterView,
      meta: { guestOnly: true },
    },
    {
      path: '/profile',
      name: 'profile',
      component: ProfileView,
      meta: { requiresAuth: true },
    },
    {
      path: '/on-loan',
      name: 'on-loan',
      component: OnLoanView,
      meta: { requiresAdmin: true },
    },
    {
      path: '/manage-loans',
      name: 'manage-loans',
      component: ManageLoansView,
      meta: { requiresAdmin: true },
    },
    {
      path: '/reports',
      name: 'reports',
      component: ReportsView,
      meta: { requiresAdmin: true },
    },
    {
      path: '/copies',
      name: 'copies-manage',
      component: CopiesManageView,
      meta: { requiresAdmin: true },
    },
  ],
})

// защита роутов по ролям
router.beforeEach((to, from, next) => {
  const auth = useAuthStore()

  if (to.meta.requiresAuth && !auth.isAuthenticated) {
    return next({ name: 'login' })
  }

  if (to.meta.requiresAdmin && !auth.isAdmin) {
    return next({ name: 'books' })
  }

  if (to.meta.guestOnly && auth.isAuthenticated) {
    return next({ name: 'books' })
  }

  return next()
})

export default router
