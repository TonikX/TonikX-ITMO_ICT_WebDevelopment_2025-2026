import { createRouter, createWebHistory } from 'vue-router';
import LoginPage from '@/views/LoginPage.vue';
import RegisterPage from '@/views/RegisterPage.vue';
import RoomsPage from '@/views/RoomsPage.vue';
import ClientPage from '@/views/ClientPage.vue';
import EmployeePage from '@/views/EmployeePage.vue';
import Profile from '@/views/Profile.vue';
import SchedulePage from '@/views/SchedulePage.vue';

const routes = [
  {
    path: '/',
    redirect: '/login',
  },
  {
    path: '/login',
    name: 'login',
    component: LoginPage,
  },
  {
    path: '/register',
    name: 'register',
    component: RegisterPage,
  },
  {
    path: '/rooms',
    name: 'rooms',
    component: RoomsPage,
  },
  {
    path: '/clients',
    name: 'clients',
    component: ClientPage,
  },
  {
    path: '/employees',
    name: 'employees',
    component: EmployeePage,
  },
  {
    path: '/profile',
    name: 'profile',
    component: Profile,
  },
  {
    path: '/schedule',
    name: 'schedule',
    component: SchedulePage,
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
