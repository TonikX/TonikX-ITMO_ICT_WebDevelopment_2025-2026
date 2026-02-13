import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../stores/auth'

// ===== ПУБЛИЧНЫЕ СТРАНИЦЫ =====
const LoginView = () => import('../views/LoginView.vue')
const RegisterView = () => import('../views/RegisterView.vue')
const BooksView = () => import('../views/BooksView.vue')

// ===== СТРАНИЦЫ ЧИТАТЕЛЕЙ =====
const ProfileView = () => import('../views/ProfileView.vue')
const LinkReaderView = () => import('../views/LinkReaderView.vue')

// ===== СТРАНИЦЫ АДМИНИСТРАТОРА =====
const AdminLayout = () => import('../views/Admin/AdminLayout.vue')
const AdminDashboard = () => import('../views/Admin/AdminDashboard.vue')
const AdminReaders = () => import('../views/Admin/AdminReaders.vue')
const AdminReaderDetail = () => import('../views/Admin/AdminReaderDetail.vue')
const AdminReaderRegister = () => import('../views/Admin/AdminReaderRegister.vue')
const AdminBooks = () => import('../views/Admin/AdminBooks.vue')
const AdminIssueBook = () => import('../views/Admin/AdminIssueBookView.vue')
const AdminBookAdd = () => import('../views/Admin/AdminBookAdd.vue')
const AdminBookDecommission = () => import('../views/Admin/AdminBookDecommission.vue')
const AdminCopyTransfer = () => import('../views/Admin/AdminCopyTransfer.vue')
const AdminReports = () => import('../views/ReportsView.vue')
const OnLoanView = () => import('../views/OnLoanView.vue')
const ManageLoansView = () => import('../views/ManageLoansView.vue')

const routes = [
  { path: '/', redirect: '/books' },

  // ===== ПУБЛИЧНЫЕ =====
  { path: '/login', name: 'login', component: LoginView, meta: { guestOnly: true } },
  { path: '/register', name: 'register', component: RegisterView, meta: { guestOnly: true } },
  { path: '/books', name: 'books', component: BooksView, meta: { requiresAuth: false } },

  // ===== ЧИТАТЕЛИ =====
  { path: '/profile', name: 'profile', component: ProfileView, meta: { requiresAuth: true } },
  { path: '/link-reader', name: 'link-reader', component: LinkReaderView, meta: { requiresAuth: true } },

  // ===== АДМИН-ПАНЕЛЬ =====
  {
    path: '/admin',
    component: AdminLayout,
    meta: { requiresAdmin: true },
    children: [
      { path: '', name: 'admin-dashboard', component: AdminDashboard, meta: { requiresAdmin: true } },
      { path: 'readers', name: 'admin-readers', component: AdminReaders, meta: { requiresAdmin: true } },
      { path: 'readers/register', name: 'admin-reader-register', component: AdminReaderRegister, meta: { requiresAdmin: true } },
      { path: 'readers/:id', name: 'admin-reader-detail', component: AdminReaderDetail, props: true, meta: { requiresAdmin: true } },
      { path: 'books', name: 'admin-books', component: AdminBooks, meta: { requiresAdmin: true } },
      { path: 'issue-book', name: 'admin-issue-book', component: AdminIssueBook, meta: { requiresAdmin: true } },
      { path: 'books/add', name: 'admin-book-add', component: AdminBookAdd, meta: { requiresAdmin: true } },
      { path: 'books/decommission', name: 'admin-book-decommission', component: AdminBookDecommission, meta: { requiresAdmin: true } },
      { path: 'copies/transfer', name: 'admin-copy-transfer', component: AdminCopyTransfer, meta: { requiresAdmin: true } },
      { path: 'on-loan', name: 'on-loan', component: OnLoanView, meta: { requiresAdmin: true } },
      { path: 'manage-loans', name: 'manage-loans', component: ManageLoansView, meta: { requiresAdmin: true } },
      { path: 'reports', name: 'reports', component: AdminReports, meta: { requiresAdmin: true } }
    ]
  },

  // ===== 404 =====
  { path: '/:pathMatch(.*)*', redirect: '/books' }
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior: () => ({ top: 0 })
})

// ===== ЗАЩИТА МАРШРУТОВ =====
router.beforeEach((to, from, next) => {
  const auth = useAuthStore()

  if (to.meta.requiresAdmin) {
    if (!auth.isAuthenticated) return next('/login')
    if (!auth.isAdmin) return next('/books')
    return next()
  }
  if (to.meta.requiresAuth && !auth.isAuthenticated) return next('/login')
  if (to.meta.guestOnly && auth.isAuthenticated) return next('/books')

  next()
})

export default router