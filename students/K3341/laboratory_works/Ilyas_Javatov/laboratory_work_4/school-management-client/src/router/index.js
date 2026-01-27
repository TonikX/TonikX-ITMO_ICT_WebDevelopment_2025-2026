import { createRouter, createWebHistory } from 'vue-router'
import store from '../store'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: () => import('../views/Home.vue'),
    meta: { title: 'Главная' }
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('../components/Auth/Login.vue'),
    meta: {
      title: 'Вход в систему',
      guest: true
    }
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('../components/Auth/Register.vue'),
    meta: {
      title: 'Регистрация',
      guest: true
    }
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: () => import('../views/Dashboard.vue'),
    meta: {
      title: 'Панель управления',
      requiresAuth: true
    }
  },
  {
    path: '/teachers',
    name: 'Teachers',
    component: () => import('../views/TeachersView.vue'),
    meta: {
      title: 'Учителя',
      requiresAuth: true
    }
  },
  {
    path: '/students',
    name: 'Students',
    component: () => import('../views/StudentsView.vue'),
    meta: {
      title: 'Ученики',
      requiresAuth: true
    }
  },
  {
    path: '/classes',
    name: 'Classes',
    component: () => import('../views/ClassesView.vue'),
    meta: {
      title: 'Классы',
      requiresAuth: true
    }
  },
  {
    path: '/classrooms',
    name: 'Classrooms',
    component: () => import('../views/ClassroomsView.vue'),
    meta: {
      title: 'Кабинеты',
      requiresAuth: true
    }
  },
  {
    path: '/schedule',
    name: 'Schedule',
    component: () => import('../views/ScheduleView.vue'),
    meta: {
      title: 'Расписание',
      requiresAuth: true
    }
  },
  {
    path: '/reports',
    name: 'Reports',
    component: () => import('../views/ReportsView.vue'),
    meta: {
      title: 'Отчеты',
      requiresAuth: true
    }
  },
  {
    path: '/profile',
    name: 'Profile',
    component: () => import('../components/Auth/Profile.vue'),
    meta: {
      title: 'Профиль',
      requiresAuth: true
    }
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: () => import('../views/NotFound.vue'),
    meta: { title: 'Страница не найдена' }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach(async (to, from, next) => {
  // Устанавливаем заголовок страницы
  document.title = `${to.meta?.title || 'School Management'} | ${process.env.VUE_APP_TITLE || 'School System'}`

  // Проверяем аутентификацию
  const requiresAuth = to.matched.some(record => record.meta.requiresAuth)
  const guestOnly = to.matched.some(record => record.meta.guest)

  // Проверяем токен в localStorage
  const token = localStorage.getItem('token')
  const isAuthenticated = !!token

  if (requiresAuth && !isAuthenticated) {
    // Если требуется аутентификация, но пользователь не авторизован
    next({ name: 'Login' })
  } else if (guestOnly && isAuthenticated) {
    // Если страница только для гостей, но пользователь авторизован
    next({ name: 'Dashboard' })
  } else {
    // Все проверки пройдены
    next()
  }
})

export default router