import Account from '../views/Account.vue'
import Home from '../views/Dashboard.vue'
import FileView from '../views/FileList.vue'
import FolderView from '../views/FolderView.vue'
import Login from '../views/Login.vue'
import Register from '../views/Register.vue'

export default [
  { path: '/', name: 'home', component: Home, meta: { requiresAuth: true } },
  { path: '/files', name: 'files', component: FileView, meta: { requiresAuth: true } },
  { path: '/folders/:id', name: 'folder', component: FolderView, meta: { requiresAuth: true } },
  { path: '/account', name: 'account', component: Account, meta: { requiresAuth: true } },
  { path: '/login', name: 'login', component: Login },
  { path: '/register', name: 'register', component: Register }
]