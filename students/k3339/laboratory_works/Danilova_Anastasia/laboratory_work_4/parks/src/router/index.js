import { createRouter, createWebHistory } from "vue-router";
import LoginView from "@/views/LoginView.vue";
import HomeView from "@/views/HomeView.vue";
import RegisterView from "@/views/RegisterView.vue";
import DashboardView from "@/views/DashboardView.vue";
import ObjectDetailView from "@/views/ObjectDetailView.vue";
import ObjectEditView from "@/views/ObjectEditView.vue";
import ObjectCreateView from "@/views/ObjectCreateView.vue";
import UserSettingsView from "../views/UserSettingsView.vue";

import { useAuthStore } from "@/store/auth";

const routes = [
  {
    path: "/",
    name: "home",
    component: HomeView,
  },
  {
    path: "/login",
    name: "login",
    component: LoginView,
  },
  {
    path: "/register",
    name: "register",
    component: RegisterView,
  },
  {
    path: "/dashboard",
    name: "dashboard",
    component: DashboardView,
    meta: { requiresAuth: true },
  },
  {
    path: "/settings",
    name: "UserSettings",
    component: UserSettingsView,
    meta: { requiresAuth: true },
  },
  {
    path: "/objects/:id",
    name: "object-detail",
    component: ObjectDetailView,
    meta: { requiresAuth: true },
  },
  {
    path: "/objects/:id/edit",
    name: "object-edit",
    component: ObjectEditView,
    meta: { requiresAuth: true },
  },
  {
    path: "/objects/new",
    name: "object-create",
    component: ObjectCreateView,
    meta: { requiresAuth: true },
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach((to, from, next) => {
  const authStore = useAuthStore();

  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    next("/login");
  } else if (
    (to.path === "/login" || to.path === "/register") &&
    authStore.isAuthenticated
  ) {
    next("/dashboard");
  } else {
    next();
  }
});

export default router;
