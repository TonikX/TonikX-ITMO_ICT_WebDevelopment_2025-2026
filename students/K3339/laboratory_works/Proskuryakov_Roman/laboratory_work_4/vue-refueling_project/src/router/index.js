import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../stores/auth'

// Импорт компонентов (создадим позже)
import LoginView from '../views/LoginView.vue'
import DashboardView from '../views/DashboardView.vue'
import FuelSaleView from '../views/FuelSaleView.vue'
import SalesSummaryView from '../views/SalesSummaryView.vue'

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: LoginView,
    meta: { requiresGuest: true }
  },
  {
    path: '/',
    name: 'Dashboard',
    component: DashboardView,
    meta: { requiresAuth: true }
  },
  {
    path: '/fuel-sale',
    name: 'FuelSale',
    component: FuelSaleView,
    meta: { requiresAuth: true }
  },
  {
    path: '/sales-summary/:modelName?',
    name: 'SalesSummary',
    component: SalesSummaryView,
    meta: { requiresAuth: true }
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// Глобальный навигационный хук для проверки авторизации
router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()
  
  // Если маршрут требует авторизации
  if (to.matched.some(record => record.meta.requiresAuth)) {
    if (!authStore.isAuthenticated) {
      next('/login')
    } else {
      next()
    }
  } 
  // Если маршрут доступен только для гостей (неавторизованных)
  else if (to.matched.some(record => record.meta.requiresGuest)) {
    if (authStore.isAuthenticated) {
      next('/')
    } else {
      next()
    }
  } 
  // Для всех остальных маршрутов
  else {
    next()
  }
})

export default router