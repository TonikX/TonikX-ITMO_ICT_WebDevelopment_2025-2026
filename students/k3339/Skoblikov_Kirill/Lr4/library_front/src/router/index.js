import { createRouter, createWebHistory } from 'vue-router';
import Main from "@/pages/MainPage.vue";
import Register from "@/pages/RegisterFormPage.vue";
import Login from "@/pages/LoginFormPage.vue";
import Book from "@/pages/BooksPage.vue";
import Reader from "@/pages/ReadersPage.vue";
import Reading from "@/pages/ReadingPage.vue";
import Stats from "@/pages/StatsPage.vue";
import Hi from "@/pages/HiPage.vue";
import AuthLayout from "@/components/AuthLayout.vue";
import Halls from "@/pages/HallPage.vue"

const routes = [
  {
    path: "/",
    component: Main
  },
  {
    path: "/register",
    component: Register
  },
  {
    path: "/login",
    component: Login
  },
  {
    path: "/hi",
    component: Hi
  },
  {
      path: '/app',
      component: AuthLayout,
      meta: { requiresAuth: true },
      children: [
        {path: 'books', component: Book },
        {path: 'readers', component: Reader},
        {path: 'reading', component: Reading},
        {path: 'stats', component: Stats},
        {path: 'halls', component: Halls}
      ]
    }
]

const router = createRouter({
  routes,
  history: createWebHistory(import.meta.env.BASE_URL),
})

export default router;
