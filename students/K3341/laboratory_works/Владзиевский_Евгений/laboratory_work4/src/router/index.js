import { createRouter, createWebHistory } from 'vue-router'
import { isAuthenticated } from '../stores/auth'

const routes = [
  { path: '/', name: 'latest', component: () => import('../views/FeedLatest.vue'), meta: { requiresAuth: true } },
  { path: '/recommended', name: 'recommended', component: () => import('../views/RecommendedFeed.vue'), meta: { requiresAuth: true } },
  { path: '/post/:id', name: 'post', component: () => import('../views/PostDetails.vue'), meta: { requiresAuth: true } },
  { path: '/create', name: 'create', component: () => import('../views/CreatePost.vue'), meta: { requiresAuth: true } },
  { path: '/my', name: 'myPosts', component: () => import('../views/MyPosts.vue'), meta: { requiresAuth: true } },
  { path: '/user/:id/posts', name: 'userPosts', component: () => import('../views/UserPosts.vue'), meta: { requiresAuth: true } },
  { path: '/profile', name: 'profile', component: () => import('../views/ProfileView.vue'), meta: { requiresAuth: true } },
  { path: '/login', name: 'login', component: () => import('../views/LoginView.vue') },
  { path: '/register', name: 'register', component: () => import('../views/RegisterView.vue') },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach((to, from, next) => {
  if (to.meta.requiresAuth && !isAuthenticated()) {
    return next({ name: 'login', query: { redirect: to.fullPath } })
  }
  if ((to.name === 'login' || to.name === 'register') && isAuthenticated()) {
    return next({ name: 'latest' })
  }
  return next()
})

export default router
