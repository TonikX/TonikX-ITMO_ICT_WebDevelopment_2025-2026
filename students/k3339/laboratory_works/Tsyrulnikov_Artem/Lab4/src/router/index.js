import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  { path: '/login', name: 'Login', component: () => import('@/views/Login.vue') },
  { path: '/register', name: 'Register', component: () => import('@/views/Register.vue') },
  { path: '/', name: 'Home', component: () => import('@/views/Home.vue'), meta: { auth: true } },
  { path: '/profile', name: 'Profile', component: () => import('@/views/Profile.vue'), meta: { auth: true } },
  { path: '/clients', name: 'Clients', component: () => import('@/views/Clients.vue'), meta: { auth: true } },
  { path: '/services', name: 'Services', component: () => import('@/views/Services.vue'), meta: { auth: true } },
  { path: '/orders', name: 'Orders', component: () => import('@/views/Orders.vue'), meta: { auth: true } },
  { path: '/payments', name: 'Payments', component: () => import('@/views/Payments.vue'), meta: { auth: true } },
]

const router = createRouter({ history: createWebHistory(), routes })

router.beforeEach((to, from, next) => {
  const isAuth = !!localStorage.getItem('access')
  if (to.meta.auth && !isAuth) next('/login')
  else if ((to.name === 'Login' || to.name === 'Register') && isAuth) next('/')
  else next()
})

export default router
