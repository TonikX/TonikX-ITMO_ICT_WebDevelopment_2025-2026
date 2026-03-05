import { createRouter, createWebHistory } from "vue-router"

import VacanciesView from "../views/VacanciesView.vue"
import ApplicantsView from "../views/ApplicantsView.vue"
import AnalyticsView from "../views/AnalyticsView.vue"

import LoginView from "../views/LoginView.vue"
import RegisterView from "../views/RegisterView.vue"
import AccountView from "../views/AccountView.vue"

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: "/", redirect: "/vacancies" },

    { path: "/vacancies", component: VacanciesView },
    { path: "/applicants", component: ApplicantsView },
    { path: "/analytics", component: AnalyticsView },

    { path: "/login", component: LoginView },
    { path: "/register", component: RegisterView },
    { path: "/account", component: AccountView },
  ],
})

export default router