import LoginView from '../views/LoginView.vue'
import RegisterView from '../views/RegisterView.vue'
import RoomsView from '../views/RoomsView.vue'
import RoomDetailsView from '../views/RoomDetailsView.vue'
import BookingView from '../components/BookingView.vue'
import MyBookingsView from '../views/MyBookingsView.vue'
import EditBookingView from '../views/EditBookingView.vue'
import { useAuthStore } from '../store/auth'

// список маршрутов приложения
export const routes = [
  { path: '/', redirect: '/rooms' },
  { path: '/login', component: LoginView },
  { path: '/register', component: RegisterView },
  {
    path: '/my-bookings',
    component: MyBookingsView,
    meta: { requiresAuth: true }
  },
  {
    path: '/my-bookings/:id/edit',
    component: EditBookingView,
    meta: { requiresAuth: true }
  },
  {
    path: '/rooms',
    component: RoomsView,
    meta: { requiresAuth: true }
  },
  {
    path: '/rooms/:id',
    component: RoomDetailsView,
    meta: { requiresAuth: true }
  },
  {
    path: '/rooms/:id/book',
    component: BookingView,
    meta: { requiresAuth: true }
  }
]

// простая функция для подключения глобального гуарда
export function setupRouterGuards(router) {
  // проверяем авторизацию перед переходом
  router.beforeEach((to, from, next) => {
    const auth = useAuthStore()

    if (to.meta.requiresAuth && !auth.token.value) {
      next('/login')
    } else if ((to.path === '/login' || to.path === '/register') && auth.token.value) {
      next('/rooms')
    } else {
      next()
    }
  })
}

