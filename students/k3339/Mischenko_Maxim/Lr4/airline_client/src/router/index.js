import { createRouter, createWebHistory } from 'vue-router'
import Login from '../views/Login.vue'
import Register from '../views/Register.vue'
import Profile from '../views/Profile.vue'

import Planes from '../views/Planes.vue'
import Routes from '../views/Routes.vue'
import Seats from '../views/Seats.vue'
import Tickets from '../views/Tickets.vue'
import MyTickets from '../views/MyTickets.vue'

const routes = [
  { path: '/', redirect: '/planes' },
  { path: '/login', component: Login },
  { path: '/register', component: Register },
  { path: '/profile', component: Profile },
  
  { path: '/planes', component: Planes },
  { path: '/routes', component: Routes },
  { path: '/seats', component: Seats },
  { path: '/tickets', component: Tickets },
  { path: '/my-tickets', component: MyTickets },
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  const publicPages = ['/login', '/register'];
  const authRequired = !publicPages.includes(to.path);
  const loggedIn = localStorage.getItem('auth_token');

  if (authRequired && !loggedIn) {
    return next('/login');
  }
  next();
})

export default router
