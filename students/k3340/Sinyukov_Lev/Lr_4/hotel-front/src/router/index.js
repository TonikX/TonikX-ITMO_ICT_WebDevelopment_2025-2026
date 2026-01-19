import { createRouter, createWebHistory } from "vue-router";
import { useAuthStore } from "@/stores/auth";

const routes = [
  { path: "/login", component: () => import("@/views/Login.vue") },
  { path: "/register", component: () => import("@/views/Register.vue") },

  {
    path: "/",
    component: () => import("@/layouts/MainLayout.vue"),
    meta: { auth: true },
    children: [
      { path: "", component: () => import("@/views/dashboard/Home.vue") },

      { path: "profile", component: () => import("@/views/Profile.vue") },

      { path: "rooms", component: () => import("@/views/crud/Rooms.vue") },
      { path: "clients", component: () => import("@/views/crud/Clients.vue") },
      { path: "stays", component: () => import("@/views/crud/Stays.vue") },
      { path: "employees", component: () => import("@/views/crud/Employees.vue") },
      { path: "schedules", component: () => import("@/views/crud/Schedules.vue") },

      { path: "analytics/free-rooms", component: () => import("@/views/analytics/FreeRooms.vue") },
      { path: "analytics/clients-from-city", component: () => import("@/views/analytics/ClientsFromCity.vue") },
      { path: "analytics/clients-in-room", component: () => import("@/views/analytics/ClientsInRoom.vue") },
      { path: "analytics/who-cleaned", component: () => import("@/views/analytics/WhoCleaned.vue") },
      { path: "analytics/clients-overlap", component: () => import("@/views/analytics/ClientsOverlap.vue") },

      { path: "reports/quarter", component: () => import("@/views/reports/QuarterReport.vue") },
    ],
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach(async (to) => {
  const auth = useAuthStore();

  // публичные страницы
  if (!to.meta?.auth) {
    // если уже залогинен — не пускаем обратно на login/register
    if ((to.path === "/login" || to.path === "/register") && auth.isAuthed) {
      return "/";
    }
    return true;
  }

  // защищённые страницы
  if (!auth.isAuthed) return "/login";

  // токен есть, но user ещё не подтянут — подтягиваем
  if (!auth.user) {
    try {
      await auth.fetchMe();
    } catch {
      auth.logout();
      return "/login";
    }
  }

  return true;
});

export default router;