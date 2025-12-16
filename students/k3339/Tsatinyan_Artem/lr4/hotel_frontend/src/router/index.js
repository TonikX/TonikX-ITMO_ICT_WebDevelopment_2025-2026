import { createRouter, createWebHistory } from 'vue-router'
import LoginView from '../views/LoginView.vue'
import RegisterView from '../views/RegisterView.vue'
import ProfileView from '../views/ProfileView.vue'
import RoomsView from '../views/RoomsView.vue'
import RoomDetailsView from '../views/RoomDetailsView.vue'
import StaysView from '../views/StaysView.vue'
import DashboardView from '../views/DashboardView.vue'
import BookingView from '../views/BookingView.vue'
import StaffView from '../views/StaffView.vue'
import StaffDetailsView from '../views/StaffDetailsView.vue'

const routes = [
  { path: '/', redirect: '/dashboard' },
  { path: '/login', component: LoginView },
  { path: '/register', component: RegisterView },
  { path: '/profile', component: ProfileView },
  { path: '/dashboard', component: DashboardView },
  { path: '/rooms', component: RoomsView },
  { path: '/rooms/:id', component: RoomDetailsView, props: true },
  { path: '/stays', component: StaysView },
  { path: '/booking', component: BookingView },
  { path: '/staff', component: StaffView },
  { path: '/staff/:id', component: StaffDetailsView, props: true },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
