import { createRouter as _createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const AuthLayout = () => import('../layouts/AuthLayout.vue')
const LoginPage = () => import('../views/auth/LoginPage.vue')
const RegisterPage = () => import('../views/auth/RegisterPage.vue')
const ProfilePage = () => import('../views/auth/ProfilePage.vue')

const DashboardPage = () => import('../views/DashboardPage.vue')
const CompaniesPage = () => import('../views/entities/CompaniesPage.vue')
const AircraftsPage = () => import('../views/entities/AircraftsPage.vue')
const AirportsPage = () => import('../views/entities/AirportsPage.vue')
const EmployeesPage = () => import('../views/entities/EmployeesPage.vue')
const CrewsPage = () => import('../views/entities/CrewsPage.vue')
const CrewMembersPage = () => import('../views/entities/CrewMembersPage.vue')
const FlightsPage = () => import('../views/entities/FlightsPage.vue')
const FlightDetailsPage = () => import('../views/entities/FlightDetailsPage.vue')
const TransitStopsPage = () => import('../views/entities/TransitStopsPage.vue')
const ReportsPage = () => import('../views/ReportsPage.vue')

export function createRouter() {
  const router = _createRouter({
    history: createWebHistory(),
    routes: [
      {
        path: '/auth',
        component: AuthLayout,
        meta: { public: true },
        children: [
          { path: 'login', name: 'login', component: LoginPage, meta: { title: 'Вход' } },
          { path: 'register', name: 'register', component: RegisterPage, meta: { title: 'Регистрация' } },
        ],
      },
      {
        path: '/',
        component: DashboardPage,
        children: [
          { path: '', redirect: '/companies' },
          { path: 'profile', name: 'profile', component: ProfilePage, meta: { title: 'Профиль' } },
          { path: 'companies', name: 'companies', component: CompaniesPage, meta: { title: 'Компании' } },
          { path: 'aircrafts', name: 'aircrafts', component: AircraftsPage, meta: { title: 'Самолёты' } },
          { path: 'airports', name: 'airports', component: AirportsPage, meta: { title: 'Аэропорты' } },
          { path: 'employees', name: 'employees', component: EmployeesPage, meta: { title: 'Сотрудники' } },
          { path: 'crews', name: 'crews', component: CrewsPage, meta: { title: 'Экипажи' } },
          { path: 'crew-members', name: 'crewMembers', component: CrewMembersPage, meta: { title: 'Состав экипажа' } },
          { path: 'flights', name: 'flights', component: FlightsPage, meta: { title: 'Рейсы' } },
          { path: 'flights/:id', name: 'flightDetails', component: FlightDetailsPage, props: true, meta: { title: 'Детали рейса' } },
          { path: 'transit-stops', name: 'transitStops', component: TransitStopsPage, meta: { title: 'Транзитные остановки' } },
          { path: 'reports', name: 'reports', component: ReportsPage, meta: { title: 'Запросы/Отчёты' } },
        ],
      },
      { path: '/:pathMatch(.*)*', redirect: '/' },
    ],
  })

  router.beforeEach((to) => {
    const auth = useAuthStore()
    if (!auth.token) auth.hydrate()
    if (to.meta.public) return true
    if (!auth.isAuthenticated) {
      return { name: 'login', query: { next: to.fullPath } }
    }
    return true
  })

  return router
}
