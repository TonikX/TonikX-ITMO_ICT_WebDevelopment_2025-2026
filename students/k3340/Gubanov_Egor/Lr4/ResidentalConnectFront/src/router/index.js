import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { isDispatcher } from '@/utils/roleUtils'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: () => import('@/views/Home.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/Login.vue'),
    meta: { requiresGuest: true },
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('@/views/Register.vue'),
    meta: { requiresGuest: true },
  },
  {
    path: '/profile',
    name: 'Profile',
    component: () => import('@/views/Profile.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/buildings',
    name: 'BuildingsList',
    component: () => import('@/views/BuildingsList.vue'),
    meta: { requiresAuth: true, requiresRole: 'dispatcher' },
  },
  {
    path: '/buildings/new',
    name: 'BuildingNew',
    component: () => import('@/views/BuildingForm.vue'),
    meta: { requiresAuth: true, requiresRole: 'dispatcher' },
  },
  {
    path: '/buildings/:id',
    name: 'BuildingDetail',
    component: () => import('@/views/BuildingDetail.vue'),
    meta: { requiresAuth: true, requiresRole: 'dispatcher' },
  },
  {
    path: '/buildings/:id/edit',
    name: 'BuildingEdit',
    component: () => import('@/views/BuildingForm.vue'),
    meta: { requiresAuth: true, requiresRole: 'dispatcher' },
  },
  {
    path: '/buildings/statistics',
    name: 'BuildingsStatistics',
    component: () => import('@/views/BuildingsStatistics.vue'),
    meta: { requiresAuth: true, requiresRole: 'dispatcher' },
  },
  {
    path: '/apartments',
    name: 'ApartmentsList',
    component: () => import('@/views/ApartmentsList.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/apartments/new',
    name: 'ApartmentNew',
    component: () => import('@/views/ApartmentForm.vue'),
    meta: { requiresAuth: true, requiresRole: 'dispatcher' },
  },
  {
    path: '/apartments/:id',
    name: 'ApartmentDetail',
    component: () => import('@/views/ApartmentDetail.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/apartments/:id/edit',
    name: 'ApartmentEdit',
    component: () => import('@/views/ApartmentForm.vue'),
    meta: { requiresAuth: true, requiresRole: 'dispatcher' },
  },
  {
    path: '/service-requests',
    name: 'ServiceRequestsList',
    component: () => import('@/views/ServiceRequestsList.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/service-requests/new',
    name: 'ServiceRequestNew',
    component: () => import('@/views/ServiceRequestForm.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/service-requests/my',
    name: 'MyRequests',
    component: () => import('@/views/MyRequests.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/service-requests/assigned',
    name: 'AssignedRequests',
    component: () => import('@/views/AssignedRequests.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/service-requests/:id',
    name: 'ServiceRequestDetail',
    component: () => import('@/views/ServiceRequestDetail.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/service-requests/:id/edit',
    name: 'ServiceRequestEdit',
    component: () => import('@/views/ServiceRequestForm.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/service-requests/statistics',
    name: 'ServiceRequestsStatistics',
    component: () => import('@/views/ServiceRequestsStatistics.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/meter-readings',
    name: 'MeterReadingsList',
    component: () => import('@/views/MeterReadingsList.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/meter-readings/new',
    name: 'MeterReadingNew',
    component: () => import('@/views/MeterReadingForm.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/meter-readings/:id',
    name: 'MeterReadingDetail',
    component: () => import('@/views/MeterReadingDetail.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/meter-readings/:id/edit',
    name: 'MeterReadingEdit',
    component: () => import('@/views/MeterReadingForm.vue'),
    meta: { requiresAuth: true, requiresRole: 'dispatcher' },
  },
  {
    path: '/meter-readings/statistics',
    name: 'MeterReadingsStatistics',
    component: () => import('@/views/MeterReadingsStatistics.vue'),
    meta: { requiresAuth: true },
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()
  const isAuthenticated = authStore.isAuthenticated
  const user = authStore.user

  if (to.meta.requiresAuth && !isAuthenticated) {
    next({ name: 'Login', query: { redirect: to.fullPath } })
  } else if (to.meta.requiresGuest && isAuthenticated) {
    next({ name: 'Home' })
  } else if (to.meta.requiresRole) {
    if (to.meta.requiresRole === 'dispatcher' && !isDispatcher(user)) {
      next({ name: 'Home' })
    } else {
      next()
    }
  } else {
    next()
  }
})

export default router
