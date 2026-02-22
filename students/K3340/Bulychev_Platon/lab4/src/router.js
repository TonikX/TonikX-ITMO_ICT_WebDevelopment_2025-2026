import { createRouter, createWebHistory } from 'vue-router'
import Login from './views/Login.vue'
import Register from './views/Register.vue'
import Profile from './views/Profile.vue'
import Drivers from './views/Drivers.vue'
import Buses from './views/Buses.vue'
import BusTypes from './views/BusTypes.vue'
import Routes from './views/Routes.vue'
import Schedules from './views/Schedules.vue'
import Absences from './views/Absences.vue'
import Report from './views/Report.vue'

const routes = [
  { path: '/login', component: Login },
  { path: '/register', component: Register },
  { path: '/profile', component: Profile },
  { path: '/', component: Drivers },
  { path: '/buses', component: Buses },
  { path: '/bus-types', component: BusTypes },
  { path: '/routes', component: Routes },
  { path: '/schedules', component: Schedules },
  { path: '/absences', component: Absences },
  { path: '/report', component: Report },
]

const router = createRouter({ history: createWebHistory(), routes })

router.beforeEach((to) => {
  const token = localStorage.getItem('token')
  if (!token && !['/login', '/register'].includes(to.path)) return '/login'
})

export default router
