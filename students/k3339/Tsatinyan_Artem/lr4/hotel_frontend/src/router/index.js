import { createRouter, createWebHistory } from 'vue-router'
import LoginView from '../views/LoginView.vue'
import RegisterView from '../views/RegisterView.vue'
import ProfileView from '../views/ProfileView.vue'
import RoomsView from '../views/RoomsView.vue'
import CheckInView from '../views/CheckInView.vue'
import FreeRoomsView from '../views/FreeRoomsView.vue'

const routes = [
  { path: '/', redirect: '/rooms' },
  { path: '/login', component: LoginView },
  { path: '/register', component: RegisterView },
  { path: '/profile', component: ProfileView },
  { path: '/rooms', component: RoomsView },
  { path: '/check-in', component: CheckInView },
  { path: '/reports/free-rooms', component: FreeRoomsView },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
