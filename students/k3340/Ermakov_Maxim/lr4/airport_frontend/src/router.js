import { createRouter, createWebHistory } from "vue-router";
import { isAuthenticated } from "./auth";

import DashboardView from "./views/DashboardView.vue";
import FlightsView from "./views/FlightsView.vue";
import FleetView from "./views/FleetView.vue";
import StaffView from "./views/StaffView.vue";
import ProfileView from "./views/ProfileView.vue";
import LoginView from "./views/LoginView.vue";
import RegisterView from "./views/RegisterView.vue";

const routes = [
  { path: "/", redirect: "/dashboard" },

  // защищённые маршруты (только для авторизованных)
  { path: "/dashboard", component: DashboardView, meta: { requiresAuth: true } },
  { path: "/flights", component: FlightsView, meta: { requiresAuth: true } },
  { path: "/fleet", component: FleetView, meta: { requiresAuth: true } },
  { path: "/staff", component: StaffView, meta: { requiresAuth: true } },
  { path: "/profile", component: ProfileView, meta: { requiresAuth: true } },

  // публичные маршруты
  { path: "/login", component: LoginView },
  { path: "/register", component: RegisterView },

  { path: "/:pathMatch(.*)*", redirect: "/dashboard" },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

// Глобальный guard
router.beforeEach((to, from, next) => {
  const publicPaths = ["/login", "/register"];

  if (!isAuthenticated.value && !publicPaths.includes(to.path)) {
    // не авторизован → только логин/регистрация
    next("/login");
  } else if (isAuthenticated.value && publicPaths.includes(to.path)) {
    // уже авторизован, но идёт на логин/регу → на dashboard
    next("/dashboard");
  } else {
    next();
  }
});

export default router;