import { createRouter, createWebHistory, type RouteRecordRaw } from 'vue-router'
import { useAuthStore } from '../store/auth'

const routes: RouteRecordRaw[] = [
  {
    path: '/login',
    name: 'login',
    component: () => import('../views/auth/LoginView.vue'),
    meta: { public: true },
  },
  {
    path: '/register',
    name: 'register',
    component: () => import('../views/auth/RegisterView.vue'),
    meta: { public: true },
  },
  {
    path: '/',
    name: 'home',
    component: () => import('../views/DashboardView.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/profile',
    name: 'profile',
    component: () => import('../views/auth/ProfileView.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/catalog/manufacturers',
    name: 'manufacturers',
    component: () => import('../views/catalog/ManufacturersView.vue'),
    meta: { requiresAuth: true, requiresAdmin: true },
  },
  {
    path: '/catalog/products',
    name: 'products',
    component: () => import('../views/catalog/ProductsView.vue'),
    meta: { requiresAuth: true, requiresAdmin: true },
  },
  {
    path: '/catalog/broker-companies',
    name: 'broker-companies',
    component: () => import('../views/catalog/BrokerCompaniesView.vue'),
    meta: { requiresAuth: true, requiresAdmin: true },
  },
  {
    path: '/catalog/brokers',
    name: 'brokers',
    component: () => import('../views/catalog/BrokersView.vue'),
    meta: { requiresAuth: true, requiresAdmin: true },
  },
  {
    path: '/trading/batches',
    name: 'batches',
    component: () => import('../views/trading/BatchesView.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/trading/batch-items',
    name: 'batch-items',
    component: () => import('../views/trading/BatchItemsView.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/reports/product-quantities',
    name: 'report-product-quantities',
    component: () => import('../views/reports/ProductQuantitiesReport.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/reports/top-manufacturer',
    name: 'report-top-manufacturer',
    component: () => import('../views/reports/TopManufacturerReport.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/reports/unsold-products',
    name: 'report-unsold-products',
    component: () => import('../views/reports/UnsoldProductsReport.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/reports/expired-items',
    name: 'report-expired-items',
    component: () => import('../views/reports/ExpiredItemsReport.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/reports/broker-salaries',
    name: 'report-broker-salaries',
    component: () => import('../views/reports/BrokerSalariesReport.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/reports/latest-trades',
    name: 'report-latest-trades',
    component: () => import('../views/reports/LatestTradesReport.vue'),
    meta: { requiresAuth: true },
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach(async (to, _from, next) => {
  const auth = useAuthStore()
  await auth.init()

  if (to.meta.requiresAuth && !auth.token) {
    return next({ name: 'login', query: { redirect: to.fullPath } })
  }

  if (to.meta.requiresAdmin && !auth.isAdmin) {
    return next({ name: 'home' })
  }

  if ((to.name === 'login' || to.name === 'register') && auth.token) {
    return next({ name: 'home' })
  }

  return next()
})

export default router

