import { createRouter, createWebHistory } from 'vue-router'

import HomePage from '../pages/HomePage.vue'
import WorkersPage from "@/pages/WorkersPage.vue";
import CellsPage from "@/pages/CellsPage.vue";
import ChickensPage from "@/pages/ChickensPage.vue";
import DietsPage from "@/pages/DietsPage.vue";
import AccountPage from "@/pages/AccountPage.vue";
import SignInPage from "@/pages/SignInPage.vue";
import WorkerPage from "@/pages/WorkerPage.vue";
import ChickenPage from "@/pages/ChickenPage.vue";
import WorkshopsPage from "@/pages/WorkshopsPage.vue";
import RowsPage from "@/pages/RowsPage.vue";
import CagesPage from "@/pages/CagesPage.vue";
import BreedsPage from "@/pages/BreedsPage.vue";
import RegisterPage from "@/pages/RegisterPage.vue";
import EggProductionsPage from "@/pages/EggProductionsPage.vue";
import ReportFactoryMonthlyPage from "@/pages/ReportFactoryMonthlyPage.vue";
import ReportBreedEggDifferencePage from "@/pages/ReportBreedEggDifferencePage.vue";

const routes = [
  {
    path: '/',
    name: 'Главная',
    component: HomePage,
    meta: { title: 'Home' }
  },
  {
    path: '/employees',
    name: 'Сотрудники',
    component: WorkersPage,
    meta: { title: 'Employees' }
  },
  {
    path: '/cells',
    name: 'Ячейки',
    component: CellsPage,
    meta: { title: 'Cells' }
  },
  {
    path: '/chickens',
    name: 'Курицы',
    component: ChickensPage,
    meta: { title: 'Chickens' }
  },
  {
    path: '/diets',
    name: 'Диеты',
    component: DietsPage,
    meta: { title: 'Diets' }
  },
  {
    path: '/account',
    name: 'Ваш профиль',
    component: AccountPage,
    meta: { title: 'Account' }
  },
  {
    path: '/sign',
    name: 'Sign',
    component: SignInPage,
    meta: { title: 'Sign' }
  },
  {
    path: '/employee/:id',
    name: 'Сотрудник',
    component: WorkerPage,
    meta: { title: 'Employee' }
  },
  {
    path: '/chickens/:id',
    name: 'Курица',
    component: ChickenPage,
    meta: { title: 'Chicken' }
  },
  {
    path: '/workshops',
    name: 'Цехи',
    component: WorkshopsPage,
    meta: { title: 'Workshops' }
  },
  {
    path: '/rows',
    name: 'Ряды',
    component: RowsPage,
    meta: { title: 'Rows' }
  },
  {
    path: '/cages',
    name: 'Клетки',
    component: CagesPage,
    meta: { title: 'Cages' }
  },
  {
    path: '/breeds',
    name: 'Породы',
    component: BreedsPage,
    meta: { title: 'Breeds' }
  },
  {
    path: '/register',
    name: 'Регистрация',
    component: RegisterPage,
    meta: { title: 'Register' }
  },
  {
    path: '/egg-production',
    name: 'Производство яиц',
    component: EggProductionsPage,
    meta: { title: 'Egg Production' }
  },
  {
    path: '/report-factory-monthly',
    name: 'Ежемесячный отчет',
    component: ReportFactoryMonthlyPage,
    meta: { title: 'Factory Monthly Report' }
  },
  {
    path: '/report-breed-egg-difference',
    name: 'Яйценоскость',
    component: ReportBreedEggDifferencePage,
    meta: { title: 'Breed egg difference report' }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
