import Hello from "@/components/Hello.vue";
import { createRouter, createWebHistory } from "vue-router";

import Warriors from "@/views/Warriors.vue"; 

const routes = [
  {
    path: '/hi',
    component: Hello
  },
  {
    path: '/warriors',
    component: Warriors
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;