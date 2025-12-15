import { createRouter, createWebHistory } from 'vue-router';

// Импорт заглушек
import Login from '../views/Login.vue';
import Register from '../views/Register.vue';
import Profile from '../views/Profile.vue';
import ClientList from '../views/ClientList.vue';
import ClientDetail from '../views/ClientDetail.vue';
import DepositList from '../views/DepositList.vue';
import CreditList from '../views/CreditList.vue';
import DepositDetail from '../views/DepositDetail.vue';
import CreditDetail from '../views/CreditDetail.vue';

const routes = [
  // Аутентификация
  { path: '/login', name: 'Login', component: Login }, // №1
  { path: '/register', name: 'Register', component: Register }, // №2
  { path: '/profile', name: 'Profile', component: Profile, meta: { requiresAuth: true } }, // №3

  // Клиенты
  { path: '/clients', name: 'ClientList', component: ClientList, meta: { requiresAuth: true } }, // №4
  { path: '/clients/create', name: 'ClientCreate', component: ClientDetail, props: { isCreating: true }, meta: { requiresAuth: true } }, // №5
  { path: '/clients/:id', name: 'ClientDetail', component: ClientDetail, props: true, meta: { requiresAuth: true } }, // №6, №7

  // Вклады
  { path: '/deposits', name: 'DepositList', component: DepositList, meta: { requiresAuth: true } }, // №8
  { path: '/deposits/create', name: 'DepositCreate', component: DepositDetail, props: { isCreating: true }, meta: { requiresAuth: true } }, // №5
  { path: '/deposits/:id', name: 'DepositDetail', component: DepositDetail, props: true, meta: { requiresAuth: true } }, // №9

  // Кредиты
  { path: '/credits', name: 'CreditList', component: CreditList, meta: { requiresAuth: true } }, // №10
  { path: '/credits/create', name: 'CreditCreate', component: CreditDetail, props: { isCreating: true }, meta: { requiresAuth: true } }, // №5
  { path: '/credits/:id', name: 'CreditDetail', component: CreditDetail, props: true, meta: { requiresAuth: true } }, // №11
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

// Глобальная проверка аутентификации
router.beforeEach((to, from, next) => {
    const isAuthenticated = localStorage.getItem('authToken');
    if (to.meta.requiresAuth && !isAuthenticated) {
        next('/login');
    } else {
        next();
    }
});

export default router;