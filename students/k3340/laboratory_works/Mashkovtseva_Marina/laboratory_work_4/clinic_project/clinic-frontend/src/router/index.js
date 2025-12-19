import { createRouter, createWebHistory } from "vue-router";
import Login from "../views/Login.vue";
import Register from "../views/Register.vue";
import Patients from "../views/Patients.vue";
import Visits from "../views/Visits.vue";
import Payments from "../views/Payments.vue";
import Profile from "../views/Profile.vue";
import Doctor from "../views/Doctor.vue";
import Room from "../views/Room.vue";

const routes = [
  { path: "/login", component: Login },
  { path: "/register", component: Register },

  {
    path: "/profile",
    component: Profile,
    meta: { requiresAuth: true },
  },
  {
    path: "/patients",
    component: Patients,
    meta: { requiresAuth: true },
  },
  {
    path: "/visits",
    component: Visits,
    meta: { requiresAuth: true },
  },
  {
    path: "/payments",
    component: Payments,
    meta: { requiresAuth: true },
  },

  {
    path: "/doctor",
    component: Doctor,
    meta: { requiresAuth: true },
  },
  {
    path: "/room",
    component: Room,
    meta: { requiresAuth: true },
  },

  { path: "/", redirect: "/login" },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem("token");

  if (to.meta.requiresAuth && !token) {
    next("/login");
  } else {
    next();
  }
});

export default router;
