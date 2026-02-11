import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../stores/auth'

// Импортируем компоненты (пока создаем пустые)
const LoginView = () => import('../views/LoginView.vue')
const RegisterView = () => import('../views/RegisterView.vue')
const BooksView = () => import('../views/BooksView.vue')
const ProfileView = () => import('../views/ProfileView.vue')
const OnLoanView = () => import('../views/OnLoanView.vue')
const ManageLoansView = () => import('../views/ManageLoansView.vue')
const ReportsView = () => import('../views/ReportsView.vue')

const routes = [
  {
    path: '/',
    redirect: '/books'
  },
  {
    path: '/login',
    name: 'login',
    component: LoginView,
    meta: { guestOnly: true }
  },
  {
    path: '/register',
    name: 'register',
    component: RegisterView,
    meta: { guestOnly: true }
  },
  {
    path: '/books',
    name: 'books',
    component: BooksView
  },
  {
    path: '/profile',
    name: 'profile',
    component: ProfileView,
    meta: { requiresAuth: true }
  },
  {
    path: '/on-loan',
    name: 'on-loan',
    component: OnLoanView,
    meta: { requiresAdmin: true }
  },
  {
    path: '/manage-loans',
    name: 'manage-loans',
    component: ManageLoansView,
    meta: { requiresAdmin: true }
  },
  {
    path: '/reports',
    name: 'reports',
    component: ReportsView,
    meta: { requiresAdmin: true }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// Защита маршрутов
router.beforeEach((to, from, next) => {
  const auth = useAuthStore()

  // Если маршрут требует авторизации
  if (to.meta.requiresAuth && !auth.isAuthenticated) {
    return next('/login')
  }

  // Если маршрут требует админских прав
  if (to.meta.requiresAdmin && (!auth.isAuthenticated || !auth.isAdmin)) {
    return next('/books')  // Перенаправляем на книги
  }

  // Если маршрут только для гостей
  if (to.meta.guestOnly && auth.isAuthenticated) {
    return next('/books')
  }

  next()
})

export default router