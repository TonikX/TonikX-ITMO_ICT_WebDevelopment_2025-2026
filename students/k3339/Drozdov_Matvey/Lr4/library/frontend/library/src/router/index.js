import { createRouter, createWebHistory } from "vue-router";
import { useAuthStore } from "@/stores/auth";

import Register from "@/views/Register.vue";
import Login from "@/views/Login.vue";
import Home from "@/views/Home.vue";
import Books from "@/views/books/Books.vue";
import AddBook from "@/views/books/AddBook.vue";
import Halls from "@/views/halls/Halls.vue";
import AddHall from "@/views/halls/AddHall.vue";
import HallDetail from "@/views/halls/HallDetail.vue";
import Readers from "@/views/readers/Readers.vue";
import AddReader from "@/views/readers/AddReader.vue";
import BookDetail from "@/views/books/BookDetail.vue";
import ReaderDetail from "@/views/readers/ReaderDetail.vue";
import Circulation from "@/views/Circulation.vue";
import Stats from "@/views/Stats.vue";

const routes = [
  { path: "/login", component: Login },
  { path: "/register", component: Register },
  { path: "/books", component: Books},
  { path: "/books/new", component: AddBook},
  { path: "/books/:id", component: BookDetail },
  { path: "/halls", component: Halls},
  { path: "/halls/new", component: AddHall },
  { path: "/halls/:id", component: HallDetail },
  { path: "/readers", component: Readers},
  { path: "/readers/new", component: AddReader },
  {path: "/readers/:id", component: ReaderDetail},
  {path: "/circulation", component: Circulation},
  {path: "/reports",component: Stats},
  { path: "/", component : Home}
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach((to) => {
  const auth = useAuthStore();

  if (to.meta.requiresAuth && !auth.isLoggedIn) {
    return "/login";
  }
});

export default router;