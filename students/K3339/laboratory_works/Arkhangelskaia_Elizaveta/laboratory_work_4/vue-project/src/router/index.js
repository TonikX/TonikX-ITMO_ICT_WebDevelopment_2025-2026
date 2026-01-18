import { createRouter, createWebHistory } from 'vue-router'
import LoginView from '@/views/LoginView.vue'
import HomeView from '@/views/HomeView.vue'
import RegisterView from '@/views/RegisterView.vue'
import ProfileView from '@/views/ProfileView.vue'
import ResidentsListView from '@/views/ResidentsListView.vue'
import ResidentDetailView from '@/views/ResidentDetailView.vue'
import ResidentEditView from '@/views/ResidentEditView.vue'
import NewResidentView from '@/views/NewResidentView.vue'
import ReservationsListView from '@/views/ReservationsListView.vue'
import ReservationDetailView from '@/views/ReservationDetailView.vue'
import ReservationEditView from '@/views/ReservationEditView.vue'
import NewReservationView from '@/views/NewReservationView.vue'
import RoomsListView from "@/views/RoomsListView.vue"
import NewRoomView from "@/views/NewRoomView.vue";
import RoomsDetailView from "@/views/RoomsDetailView.vue";
import RoomsEditView from "@/views/RoomsEditView.vue";
import ClientsByRoomView from "@/views/ClientsByRoomView.vue";
import ClientsFromCityView from '@/views/ClientsFromCityView.vue'
import ClientBookingsView from "@/views/ClientBookingsView.vue";
import ReportView from "@/views/ReportView.vue";
import CleaningPerDayView from "@/views/CleaningPerDayView.vue";
import AvailableRoomsView from "@/views/AvailableRoomsView.vue";
import WorkersListView from "@/views/WorkersListView.vue";
import WorkerEditView from "@/views/WorkerEditView.vue";
import NewWorkerView from "@/views/NewWorkerView.vue";
import CleaningListView from "@/views/CleaningListView.vue";
import CleaningEditView from "@/views/CleaningEditView.vue";
import NewCleaningView from "@/views/NewCleaningView.vue";

const routes = [
  {
    path: '/login',
    component: LoginView,
    meta: { requiresAuth: false },
  },
  {
    path: '/',
    component: HomeView,
    meta: { requiresAuth: true },
  },
  { path: '/register', component: RegisterView },
  { path: '/profile', component: ProfileView },
  { path: '/residents', component: ResidentsListView },
  { path: '/residents/:id', component: ResidentDetailView },
  { path: '/residents/:id/edit', component: ResidentEditView },
  { path: '/residents/new', component: NewResidentView },
  { path: '/reservations', component: ReservationsListView },
  { path: '/reservations/new', component: NewReservationView },
  { path: '/reservations/:id', component: ReservationDetailView },
  { path: '/reservations/:id/edit', component: ReservationEditView },
  { path: '/rooms', component: RoomsListView },
  { path: '/rooms/new', component: NewRoomView },
  { path: '/rooms/:id', component: RoomsDetailView },
  { path: '/rooms/:id/edit', component: RoomsEditView },
  { path: '/clients-by-room', component: ClientsByRoomView },
  { path: '/clients-from-city', component: ClientsFromCityView},
  { path: '/clients-with-city', component: ClientBookingsView},
  { path: '/report', component: ReportView},
  { path: '/cleaning-info-per-day', component: CleaningPerDayView},
  { path: '/available-rooms', component: AvailableRoomsView},
  { path: '/workers', component: WorkersListView},
  { path: '/workers/:id/edit', component: WorkerEditView},
  { path: '/workers/new', component: NewWorkerView},
  { path: '/cleaning', component: CleaningListView},
  { path: '/cleaning/:id/edit', component: CleaningEditView},
  { path: '/cleaning/new', component: NewCleaningView},

]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token')

  if (to.meta.requiresAuth && !token) {
    next('/login')
  } else {
    next()
  }
})

export default router
