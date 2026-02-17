import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import LoginView from '../views/LoginView.vue'
import RegisterView from '../views/RegisterView.vue'
import ReportsView from '../views/ReportsView.vue'
import RoomsView from '../views/RoomsView.vue'
import GuestsView from '../views/GuestsView.vue'
import BookingsView from '../views/BookingsView.vue'
import EmployeesView from '../views/EmployeesView.vue'
import SchedulesView from '../views/SchedulesView.vue'
import ProfileView from '../views/ProfileView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: '/', name: 'home', component: HomeView },
    { path: '/login', name: 'login', component: LoginView },
    { path: '/register', name: 'register', component: RegisterView },
    { path: '/profile', name: 'profile', component: ProfileView },
    { path: '/reports', name: 'reports', component: ReportsView },
    { path: '/rooms', name: 'rooms', component: RoomsView },
    { path: '/guests', name: 'guests', component: GuestsView },
    { path: '/bookings', name: 'bookings', component: BookingsView },
    { path: '/employees', name: 'employees', component: EmployeesView },
    { path: '/schedules', name: 'schedules', component: SchedulesView },
  ],
})

// Защита от неавторизованного доступа
router.beforeEach((to, from, next) => {
  const publicPages = ['/login', '/register']
  const authRequired = !publicPages.includes(to.path)
  const loggedIn = localStorage.getItem('auth_token')

  if (authRequired && !loggedIn) {
    next('/login')
  } else {
    next()
  }
})

export default router
