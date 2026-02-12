import { createRouter, createWebHistory } from 'vue-router'
import Login from '../views/Login.vue'
import Register from '../views/Register.vue'
import Profile from '../views/Profile.vue'
import Home from '../views/Home.vue'
import RoomTypes from '../views/RoomTypes.vue'
import Floors from '../views/Floors.vue'
import Rooms from '../views/Rooms.vue'
import Guests from '../views/Guests.vue'
import Stays from '../views/Stays.vue'
import Employees from '../views/Employees.vue'
import CleaningSchedule from '../views/CleaningSchedule.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home,
    meta: { requiresAuth: true },
  },
  {
    path: '/login',
    name: 'Login',
    component: Login,
    meta: { requiresGuest: true },
  },
  {
    path: '/register',
    name: 'Register',
    component: Register,
    meta: { requiresGuest: true },
  },
  {
    path: '/profile',
    name: 'Profile',
    component: Profile,
    meta: { requiresAuth: true },
  },
  {
    path: '/room-types',
    name: 'RoomTypes',
    component: RoomTypes,
    meta: { requiresAuth: true },
  },
  {
    path: '/floors',
    name: 'Floors',
    component: Floors,
    meta: { requiresAuth: true },
  },
  {
    path: '/rooms',
    name: 'Rooms',
    component: Rooms,
    meta: { requiresAuth: true },
  },
  {
    path: '/guests',
    name: 'Guests',
    component: Guests,
    meta: { requiresAuth: true },
  },
  {
    path: '/stays',
    name: 'Stays',
    component: Stays,
    meta: { requiresAuth: true },
  },
  {
    path: '/employees',
    name: 'Employees',
    component: Employees,
    meta: { requiresAuth: true },
  },
  {
    path: '/cleaning',
    name: 'CleaningSchedule',
    component: CleaningSchedule,
    meta: { requiresAuth: true },
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

// Навигационный guard для проверки аутентификации
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('auth_token')
  const isAuthenticated = !!token

  if (to.meta.requiresAuth && !isAuthenticated) {
    next('/login')
  } else if (to.meta.requiresGuest && isAuthenticated) {
    next('/')
  } else {
    next()
  }
})

export default router


