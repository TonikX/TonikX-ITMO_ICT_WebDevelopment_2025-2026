import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../stores/auth'

// ========== ЛЕНИВАЯ ЗАГРУЗКА ==========
// Компоненты загружаются только при переходе на маршрут

// Публичные страницы
const LoginView = () => import('../views/LoginView.vue')
const RegisterView = () => import('../views/RegisterView.vue')
const BooksView = () => import('../views/BooksView.vue')

// Страницы читателей
const ProfileView = () => import('../views/ProfileView.vue')
const LinkReaderView = () => import('../views/LinkReaderView.vue')

// Админ-страницы (только для администраторов)
const AdminDashboard = () => import('../views/Admin/AdminDashboard.vue')
const AdminReaders = () => import('../views/Admin/AdminReaders.vue')
const AdminReaderRegister = () => import('../views/Admin/AdminReaderRegister.vue')
const AdminBooks = () => import('../views/Admin/AdminBooks.vue')
const AdminIssueBook = () => import('../views/Admin/AdminIssueBookView.vue')
const AdminBookAdd = () => import('../views/Admin/AdminBookAdd.vue')
const AdminBookAddCopies = () => import('../views/Admin/AdminBookAddCopies.vue')
const AdminBookDecommission = () => import('../views/Admin/AdminBookDecommission.vue')
const AdminCopyTransfer = () => import('../views/Admin/AdminCopyTransfer.vue')
const AdminOnLoan = () => import('../views/Admin/AdminOnLoanView.vue')
const AdminManageLoans = () => import('../views/Admin/AdminManageLoansView.vue')
const ReportsView = () => import('../views/ReportsView.vue')

// ========== МАРШРУТЫ ==========
const routes = [
  { path: '/', redirect: '/books' },

  // ----- Публичные (доступны всем) -----
  { path: '/login', name: 'login', component: LoginView, meta: { guestOnly: true } },
  { path: '/register', name: 'register', component: RegisterView, meta: { guestOnly: true } },
  { path: '/books', name: 'books', component: BooksView, meta: { requiresAuth: false } },

  // ----- Читатели (только авторизованные) -----
  { path: '/profile', name: 'profile', component: ProfileView, meta: { requiresAuth: true } },
  { path: '/link-reader', name: 'link-reader', component: LinkReaderView, meta: { requiresAuth: true } },

  // ========== АДМИН-МАРШРУТЫ (все с meta: { requiresAdmin: true }) ==========

  // Дашборд
  { path: '/admin', name: 'admin-dashboard', component: AdminDashboard, meta: { requiresAdmin: true } },

  // Управление читателями
  { path: '/admin/readers', name: 'admin-readers', component: AdminReaders, meta: { requiresAdmin: true } },
  { path: '/admin/readers/register', name: 'admin-reader-register', component: AdminReaderRegister, meta: { requiresAdmin: true } },

  // Управление книгами и экземплярами
  { path: '/admin/books', name: 'admin-books', component: AdminBooks, meta: { requiresAdmin: true } },
  { path: '/admin/books/add', name: 'admin-book-add', component: AdminBookAdd, meta: { requiresAdmin: true } },
  { path: '/admin/books/add-copies', name: 'admin-book-add-copies', component: AdminBookAddCopies, meta: { requiresAdmin: true } },
  { path: '/admin/books/decommission', name: 'admin-book-decommission', component: AdminBookDecommission, meta: { requiresAdmin: true } },
  { path: '/admin/copies/transfer', name: 'admin-copy-transfer', component: AdminCopyTransfer, meta: { requiresAdmin: true } },

  // Управление выдачами
  { path: '/admin/issue-book', name: 'admin-issue-book', component: AdminIssueBook, meta: { requiresAdmin: true } },
  { path: '/admin/on-loan', name: 'admin-on-loan', component: AdminOnLoan, meta: { requiresAdmin: true } },
  { path: '/admin/manage-loans', name: 'admin-manage-loans', component: AdminManageLoans, meta: { requiresAdmin: true } },

  // Отчёты
  { path: '/admin/reports', name: 'admin-reports', component: ReportsView, meta: { requiresAdmin: true } },

  // 404
  { path: '/:pathMatch(.*)*', redirect: '/books' }
]

// ========== СОЗДАНИЕ РОУТЕРА ==========
const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior: () => ({ top: 0 })
})

// ========== ЗАЩИТА МАРШРУТОВ ==========
router.beforeEach((to, from, next) => {
  const auth = useAuthStore()

  // Админ-маршруты
  if (to.meta.requiresAdmin) {
    if (!auth.isAuthenticated) return next('/login')
    if (!auth.isAdmin) return next('/books')
    return next()
  }

  // Маршруты, требующие авторизации
  if (to.meta.requiresAuth && !auth.isAuthenticated) return next('/login')

  // Гостевые маршруты (логин/регистрация)
  if (to.meta.guestOnly && auth.isAuthenticated) return next('/books')

  next()
})

// Обработка ошибок
router.onError((error) => console.error('Ошибка навигации:', error))

export default router