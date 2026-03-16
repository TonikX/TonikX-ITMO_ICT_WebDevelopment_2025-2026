import { createRouter, createWebHistory } from "vue-router";
import { isAuthed } from "../services/auth";

import LoginView from "../views/LoginView.vue";
import RegisterView from "../views/RegisterView.vue";
import RoomsView from "../views/RoomsView.vue";
import ClientsView from "../views/ClientsView.vue";
import EmployeesView from "../views/EmployeesView.vue";
import CleaningView from "../views/CleaningView.vue";
import ReportView from "../views/ReportView.vue";
import StatsView from "../views/StatsView.vue";

const routes = [
  { path: "/", redirect: "/rooms" },
  { path: "/login", component: LoginView, meta: { public: true } },
  { path: "/register", component: RegisterView, meta: { public: true } },

  { path: "/rooms", component: RoomsView },
  { path: "/clients", component: ClientsView },
  { path: "/employees", component: EmployeesView },
  { path: "/cleaning", component: CleaningView },
  { path: "/report", component: ReportView },
  { path: "/stats", component: StatsView },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach((to) => {
  if (to.meta.public) return true;
  if (!isAuthed()) return "/login";
  return true;
});

export default router;
