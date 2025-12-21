import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    name: 'Dashboard',
    component: () => import('@/views/Dashboard.vue')
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/auth/Login.vue')
  },
  {
    path: '/drivers',
    name: 'Drivers',
    component: () => import('@/views/DriversView.vue')
  },
  {
    path: '/driver-classes',
    name: 'DriverClasses',
    component: () => import('@/views/DriverClassesView.vue')
  },
  {
    path: '/buses',
    name: 'Buses',
    component: () => import('@/views/BusesView.vue')
  },
  {
    path: '/routes',
    name: 'Routes',
    component: () => import('@/views/RoutesView.vue')
  },
  {
    path: '/workshifts',
    name: 'WorkShifts',
    component: () => import('@/views/WorkShiftsView.vue')
  },
  {
    path: '/reports',
    name: 'Reports',
    component: () => import('@/views/ReportsView.vue')
  },
  {
    path: '/bus-types',
    name: 'BusTypes',
    component: () => import('@/views/BusTypesView.vue')
  },
  {
    path: '/depots',
    name: 'Depots',
    component: () => import('@/views/DepotsView.vue')
  },

]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  const publicPages = ['/login']
  const authRequired = !publicPages.includes(to.path)
  const loggedIn = localStorage.getItem('access_token')

  if (authRequired && !loggedIn) {
    next('/login')
  } else {
    next()
  }
})

export default router
