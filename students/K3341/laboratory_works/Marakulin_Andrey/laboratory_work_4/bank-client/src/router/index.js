import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../stores/auth'

import Login from '../views/Auth/Login.vue'
import Register from '../views/Auth/Register.vue'
import ClientList from '../views/Clients/ClientList.vue'
import ClientForm from '../views/Clients/ClientForm.vue'
import ClientDetail from '../views/Clients/ClientDetail.vue'

import DepositList from '../views/Deposits/DepositList.vue'
import DepositForm from '../views/Deposits/DepositForm.vue'
import DepositDetail from '../views/Deposits/DepositDetail.vue'

import LoanList from '../views/Loans/LoanList.vue'
import LoanForm from '../views/Loans/LoanForm.vue'
import LoanDetail from '../views/Loans/LoanDetail.vue'

import PassportList from '../views/Passports/PassportList.vue'
import PassportForm from '../views/Passports/PassportForm.vue'
import PassportDetail from '../views/Passports/PassportDetail.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/login', component: Login, name: 'Login' },
    { path: '/register', component: Register, name: 'Register' },

    { path: '/clients', component: ClientList, name: 'ClientList' },
    { path: '/clients/create', component: ClientForm, name: 'ClientCreate' },
    { path: '/clients/:id', component: ClientDetail, name: 'ClientDetail', props: true },
    { path: '/clients/:id/edit', component: ClientForm, name: 'ClientEdit', props: true },

    { path: '/deposits', component: DepositList, name: 'DepositList' },
    { path: '/deposits/create', component: DepositForm, name: 'DepositCreate' },
    { path: '/deposits/:id', component: DepositDetail, name: 'DepositDetail', props: true },
    { path: '/deposits/:id/edit', component: DepositForm, name: 'DepositEdit', props: true },

    { path: '/credits', component: LoanList, name: 'LoanList' },
    { path: '/credits/create', component: LoanForm, name: 'LoanCreate' },
    { path: '/credits/:id', component: LoanDetail, name: 'LoanDetail', props: true },
    { path: '/credits/:id/edit', component: LoanForm, name: 'LoanEdit', props: true },

    { path: '/passports', component: PassportList, name: 'PassportList' },
    { path: '/passports/create', component: PassportForm, name: 'PassportCreate' },
    { path: '/passports/:id', component: PassportDetail, name: 'PassportDetail', props: true },
    { path: '/passports/:id/edit', component: PassportForm, name: 'PassportEdit', props: true },

    { path: '/', redirect: '/clients' }
  ]
})

router.beforeEach((to, from, next) => {
  const authStore = useAuthStore();
  const publicPages = ['/login', '/register'];

  if (!publicPages.includes(to.path) && !authStore.isAuthenticated) {
    next('/login');
  } else {
    next();
  }
});

export default router