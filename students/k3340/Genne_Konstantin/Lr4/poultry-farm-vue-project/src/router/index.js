import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/store/auth'

const routes = [
  { path: '/login', component: () => import('@/views/auth/LoginView.vue') },
  { path: '/register', component: () => import('@/views/auth/RegisterView.vue') },
  { path: '/profile', component: () => import('@/views/auth/ProfileView.vue'), meta: { requiresAuth: true } },

  { path: '/', component: () => import('@/views/dashboard/DashboardView.vue') },

  { path: '/breeds', component: () => import('@/views/breeds/BreedList.vue'), meta: { roles: ['employee', 'director'] } },
  { path: '/breeds/new', component: () => import('@/views/breeds/BreedForm.vue'), meta: { roles: ['employee', 'director'] } },
  { path: '/breeds/:id/edit', component: () => import('@/views/breeds/BreedForm.vue'), meta: { roles: ['employee', 'director'] } },

  { path: '/diets', component: () => import('@/views/diets/DietList.vue'), meta: { roles: ['employee', 'director'] } },
  { path: '/diets/new', component: () => import('@/views/diets/DietForm.vue'), meta: { roles: ['employee', 'director'] } },
  { path: '/diets/:id/edit', component: () => import('@/views/diets/DietForm.vue'), meta: { roles: ['employee', 'director'] } },

  { path: '/breed-diets', component: () => import('@/views/placements/BreedDietList.vue'), meta: { roles: ['employee', 'director'] } },
  { path: '/breed-diets/new', component: () => import('@/views/placements/BreedDietForm.vue'), meta: { roles: ['employee', 'director'] } },

  { path: '/cages', component: () => import('@/views/cages/CageList.vue'), meta: { roles: ['employee', 'director'] } },
  { path: '/cages/new', component: () => import('@/views/cages/CageForm.vue'), meta: { roles: ['employee', 'director'] } },
  { path: '/cages/:id', component: () => import('@/views/cages/CageDetail.vue'), meta: { roles: ['employee', 'director'] } },

  { path: '/hen-cages', component: () => import('@/views/placements/AssignCageToHen.vue'), meta: { roles: ['employee', 'director'] } },

  { path: '/employees', component: () => import('@/views/employees/EmployeeList.vue'), meta: { roles: ['director'] } },
  { path: '/employees/new', component: () => import('@/views/employees/EmployeeForm.vue'), meta: { roles: ['director'] } },
  { path: '/employees/:id/edit', component: () => import('@/views/employees/EmployeeForm.vue'), meta: { roles: ['director'] } },

  { path: '/employments', component: () => import('@/views/employees/EmploymentList.vue'), meta: { roles: ['director'] } },
  { path: '/employments/new', component: () => import('@/views/employees/EmploymentForm.vue'), meta: { roles: ['director'] } },

  { path: '/employee-cages/new', component: () => import('@/views/placements/AssignCageToEmployee.vue'), meta: { roles: ['employee', 'director'] } },
  { path: '/employee-cages', component: () => import('@/views/placements/EmployeeCageList.vue'), meta: { roles: ['employee', 'director'] } },

  { path: '/hens', component: () => import('@/views/hens/HenList.vue'), meta: { roles: ['employee', 'director'] } },
  { path: '/hens/new', component: () => import('@/views/hens/HenForm.vue'), meta: { roles: ['employee', 'director'] } },
  { path: '/hens/:id', component: () => import('@/views/hens/HenDetail.vue'), meta: { roles: ['employee', 'director'] } },

  { path: '/eggs/today', component: () => import('@/views/eggs/TodayEggRecord.vue'), meta: { roles: ['employee', 'director'] } },

  { path: '/reports/eggs-by-characteristics', component: () => import('@/views/reports/EggsByCharacteristics.vue'), meta: { roles: ['director'] } },
  { path: '/reports/top-workshop', component: () => import('@/views/reports/TopWorkshop.vue'), meta: { roles: ['director'] } },
  { path: '/reports/employee-average-eggs', component: () => import('@/views/reports/EmployeeAvgEggs.vue'), meta: { roles: ['director'] } },
  { path: '/reports/breed-distribution', component: () => import('@/views/reports/BreedDistribution.vue'), meta: { roles: ['director'] } },
  { path: '/reports/breed-efficiency-difference', component: () => import('@/views/reports/BreedEfficiencyDiff.vue'), meta: { roles: ['director'] } },
  { path: '/reports/monthly', component: () => import('@/views/reports/MonthlyReport.vue'), meta: { roles: ['director'] } },
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach(async (to, from, next) => {
  const authStore = useAuthStore()

  if (!authStore.isAuthenticated && to.path !== '/login' && to.path !== '/register') {
    return next('/login')
  }

  if (authStore.isAuthenticated && (to.path === '/login' || to.path === '/register')) {
    return next('/')
  }

  if (to.meta.roles && !authStore.role) {
    await authStore.fetchProfile()
  }

  if (to.meta.roles && !to.meta.roles.includes(authStore.role)) {
    return next('/')
  }

  next()
})

export default router