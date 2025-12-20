import {tokenStore} from "@/stores/token.js";
import Login from "@/views/Login.vue"
import Register from "@/views/Register.vue"
import Rooms from "@/views/Rooms.vue";
import Client from "@/views/Clients.vue";
// import Report from "@/views/Report.vue";
import Employee from "@/views/Employee.vue";
import Stayrecords from "@/views/Stayrecords.vue";
import Schedule from "@/views/Schedule.vue";
import {createRouter, createWebHistory} from "vue-router";
import Profile from "@/views/Profile.vue";

const routes = [
  {
      name: 'Login',
      path: '/login',
      component: Login
  },
  {
      name: 'Register',
      path: '/register',
      component: Register
  },
  {
  path: "/profile",
  component: Profile,
},
  {
      path: '/clients',
      component: Client
  },
  {
      path: '/schedule',
      component: Schedule
  },
  {
      path: '/employees',
      component: Employee
  },
  {
      path: '/rooms',
      component: Rooms
  },
  // {
  //     path: '/rooms/:id',
  //     component: RoomDetail
  // },
  {
      path: '/stay_records',
      component: Stayrecords
  },
 // {
  //    path: '/report',
  //    component: Report
 // },
  // {
  //     path: '/profile',
  //     component: Profile
  // }
  {
  path: '/',
  redirect: '/login'
  }
]

const router = createRouter({
  history: createWebHistory(), routes
})

export default router

router.beforeEach((to, from, next) => {
  const token = tokenStore().token;

  if (to.name !== 'Login' && to.name !== 'Register' && !token) {
      next({ name: 'Login' });
  } else {
      next();
  }
});