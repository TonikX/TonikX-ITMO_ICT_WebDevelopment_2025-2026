import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: () => import('@/views/HomeView.vue'),
      meta: { title: 'Главная' }
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('@/views/LoginView.vue'),
      meta: { title: 'Вход', guestOnly: true }
    },
    {
      path: '/register',
      name: 'register',
      component: () => import('@/views/RegisterView.vue'),
      meta: { title: 'Регистрация', guestOnly: true }
    },
    {
      path: '/profile',
      name: 'profile',
      component: () => import('@/views/ProfileView.vue'),
      meta: { title: 'Профиль', requiresAuth: true }
    },
    {
      path: '/companies',
      name: 'companies',
      component: () => import('@/views/CompaniesView.vue'),
      meta: { title: 'Компании' }
    },
    {
      path: '/companies/:id',
      name: 'company-detail',
      component: () => import('@/views/CompanyDetailView.vue'),
      meta: { title: 'Компания' }
    },
    {
      path: '/services',
      name: 'services',
      component: () => import('@/views/ServicesView.vue'),
      meta: { title: 'Услуги' }
    },
    {
      path: '/favorites',
      name: 'favorites',
      component: () => import('@/views/FavoritesView.vue'),
      meta: { title: 'Избранное', requiresAuth: true }
    },
    {
      path: '/requests',
      name: 'requests',
      component: () => import('@/views/RequestsView.vue'),
      meta: { title: 'Мои заявки', requiresAuth: true }
    },
    {
      path: '/reviews',
      name: 'reviews',
      component: () => import('@/views/MyReviewsView.vue'),
      meta: { title: 'Мои отзывы', requiresAuth: true }
    },
    {
      path: '/company',
      name: 'company-management',
      component: () => import('@/views/CompanyManagementView.vue'),
      meta: {
        title: 'Управление компанией',
        requiresAuth: true
      }
    },
    {
      path: '/services/:id',
      name: 'service-detail',
      component: () => import('@/views/ServiceDetailView.vue'),
      meta: { title: 'Услуга' }
    }
  ]
})

// Глобальный обработчик для изменения title страницы
router.beforeEach((to, from, next) => {
  document.title = to.meta.title ? `${to.meta.title} | Guard Market` : 'Guard Market'
  next()
})

// Глобальный защитник для аутентификации
router.beforeEach(async (to, from, next) => {
  const { useAuthStore } = await import('@/stores/auth')
  const authStore = useAuthStore()

  // Инициализация хранилища
  authStore.initialize()

  // Проверка на доступ только для гостей
  if (to.meta.guestOnly && authStore.isAuthenticated) {
    next('/')
    return
  }

  // Проверка на требование аутентификации
  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    next('/login')
    return
  }

  next()
})

export default router