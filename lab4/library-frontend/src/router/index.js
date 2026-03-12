import { createRouter, createWebHistory } from 'vue-router'
import Books from '../views/Books.vue'
import Login from '../views/Login.vue'
import Register from '../views/Register.vue'
import Profile from '../views/Profile.vue'
import BookForm from '../views/BookForm.vue'
import BookInHallForm from '../views/BookInHallForm.vue'
import Halls from '../views/Halls.vue'
import HallForm from '../views/HallForm.vue'
import HallDetail from '../views/HallDetail.vue'
import Readers from '../views/Readers.vue'
import ReaderForm from '../views/ReaderForm.vue'
import Issues from '../views/Issues.vue'
import IssueForm from '../views/IssueForm.vue'
import Reports from '../views/Reports.vue'

const routes = [
  { path: '/', redirect: '/books' },
  { path: '/books', name: 'books', component: Books },
  { path: '/books/create', name: 'book-create', component: BookForm, meta: { requiresAuth: true } },
  { path: '/books/:id/edit', name: 'book-edit', component: BookForm, meta: { requiresAuth: true } },
  { path: '/books-in-halls/:id/edit', name: 'book-in-hall-edit', component: BookInHallForm, meta: { requiresAuth: true } },
  { path: '/halls', name: 'halls', component: Halls },
  { path: '/halls/create', name: 'hall-create', component: HallForm, meta: { requiresAuth: true } },
  { path: '/halls/:id', name: 'hall-detail', component: HallDetail, meta: { requiresAuth: true } },
  { path: '/halls/:id/edit', name: 'hall-edit', component: HallForm, meta: { requiresAuth: true } },
  { path: '/readers', name: 'readers', component: Readers },
  { path: '/readers/create', name: 'reader-create', component: ReaderForm, meta: { requiresAuth: true } },
  { path: '/readers/:id/edit', name: 'reader-edit', component: ReaderForm, meta: { requiresAuth: true } },
  { path: '/issues', name: 'issues', component: Issues },
  { path: '/issues/create', name: 'issue-create', component: IssueForm, meta: { requiresAuth: true } },
  { path: '/issues/:id/edit', name: 'issue-edit', component: IssueForm, meta: { requiresAuth: true } },
  { path: '/login', name: 'login', component: Login },
  { path: '/register', name: 'register', component: Register },
  { path: '/profile', name: 'profile', component: Profile },
  { path: '/reports', name: 'reports', component: Reports, meta: { requiresAuth: true } },
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
})

router.beforeEach((to) => {
  const token = localStorage.getItem('token')
  if (to.meta && to.meta.requiresAuth && !token) {
    return { name: 'login' }
  }
  return true
})

export default router
