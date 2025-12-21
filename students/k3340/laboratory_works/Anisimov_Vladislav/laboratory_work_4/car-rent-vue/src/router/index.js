// router/index.js
import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const Dashboard = () => import('@/views/Dashboard.vue')
const LoginView = () => import('@/views/LoginView.vue')
const RegisterView = () => import('@/views/RegisterView.vue')
const ProfileView = () => import('@/views/ProfileView.vue')

const routes = [
  {
    path: '/',
    name: 'dashboard',
    component: Dashboard,
    meta: { 
      requiresAuth: true,
      title: 'Главная'
    }
  },
  {
    path: '/login',
    name: 'login',
    component: LoginView,
    meta: { 
      requiresAuth: false,
      title: 'Вход'
    }
  },
  {
    path: '/register',
    name: 'register',
    component: RegisterView,
    meta: { 
      requiresAuth: false,
      title: 'Регистрация'
    }
  },
  {
    path: '/profile',
    name: 'profile',
    component: ProfileView,
    meta: { 
      requiresAuth: true,
      title: 'Профиль'
    }
  },
  {
    path: '/cars',
    name: 'cars',
    component: () => import('@/views/CarsView.vue'),
    meta: { 
      requiresAuth: true,
      title: 'Автомобили'
    }
  },
  {
    path: '/specifications',
    name: 'specifications',
    component: () => import('@/views/SpecificationsView.vue'),
    meta: { 
      requiresAuth: true,
      title: 'Характеристики'
    }
  },
  {
    path: '/descriptions',
    name: 'descriptions',
    component: () => import('@/views/DescriptionsView.vue'),
    meta: { 
      requiresAuth: true,
      title: 'Описания'
    }
  },
  {
    path: '/contracts',
    name: 'contracts',
    component: () => import('@/views/ContractsView.vue'),
    meta: { 
      requiresAuth: true,
      title: 'Контракты'
    }
  },
  {
    path: '/clients',
    name: 'clients',
    component: () => import('@/views/ClientsView.vue'),
    meta: { 
      requiresAuth: true,
      title: 'Клиенты'
    }
  },
  {
    path: '/staff',
    name: 'staff',
    component: () => import('@/views/StaffView.vue'),
    meta: { 
      requiresAuth: true,
      title: 'Персонал'
    }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// Навигационная защита
router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()
  //authStore.initialize()
  
  // Установка заголовка страницы
  document.title = `${to.meta.title} | CarRent`
  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    next('/login')
  } else if ((to.path === '/login' || to.path === '/register') && authStore.isAuthenticated) {
    next('/')
  } else {
    next()
  }
})

export default router