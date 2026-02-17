import { createRouter, createWebHistory } from 'vue-router'
import Home from '@/views/Home.vue'
import Login from '@/views/Login.vue'
import Register from '@/views/Register.vue'
import Profile from '@/views/Profile.vue'
import Tasks from '@/views/Tasks.vue'
import TaskDetail from '@/views/TaskDetail.vue'
import Teams from '@/views/Teams.vue'
import TeamDetail from '@/views/TeamDetail.vue'
import Solutions from '@/views/Solutions.vue'
import SolutionDetail from '@/views/SolutionDetail.vue'
import Evaluations from '@/views/Evaluations.vue'

const routes = [
  {
    path: '/',
    component: Home
  },
  {
    path: '/login',
    component: Login
  },
  {
    path: '/register',
    component: Register
  },
  {
    path: '/profile',
    component: Profile
  },
  {
    path: '/tasks',
    component: Tasks
  },
  {
    path: '/tasks/:id',
    component: TaskDetail
  },
  {
    path: '/teams',
    component: Teams
  },
  {
    path: '/teams/:id',
    component: TeamDetail
  },
  {
    path: '/solutions',
    component: Solutions
  },
  {
    path: '/solutions/:id',
    component: SolutionDetail
  },
  {
    path: '/evaluations',
    component: Evaluations
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// Защита маршрутов
router.beforeEach((to, from, next) => {
  const isAuthenticated = !!localStorage.getItem('authToken')
  const publicPages = ['/', '/login', '/register']
  const isPublicPage = publicPages.includes(to.path)

  if (!isAuthenticated && !isPublicPage) {
    next('/login')
  } else if (isAuthenticated && isPublicPage) {
    next('/')
  } else {
    next()
  }
})

export default router
