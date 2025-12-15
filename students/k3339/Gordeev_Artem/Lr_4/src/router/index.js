import { createRouter, createWebHistory } from 'vue-router'

const routes = [
    {
        path: '/',
        redirect: '/dashboard'
    },
    {
        path: '/login',
        name: 'Login',
        component: () => import('@/views/auth/Login.vue'),
        meta: { layout: 'auth' }
    },
    {
        path: '/register',
        name: 'Register',
        component: () => import('@/views/auth/Register.vue'),
        meta: { layout: 'auth' }
    },
    {
        path: '/profile',
        name: 'Profile',
        component: () => import('@/views/auth/Profile.vue'),
        meta: { requiresAuth: true }
    },
    {
        path: '/dashboard',
        name: 'Dashboard',
        component: () => import('@/views/dashboard/Home.vue'),
        meta: { requiresAuth: true }
    },
    {
        path: '/books',
        name: 'Books',
        component: () => import('@/views/dashboard/Books.vue'),
        meta: { requiresAuth: true }
    },
    {
        path: '/authors',
        name: 'Authors',
        component: () => import('@/views/dashboard/Authors.vue'),
        meta: { requiresAuth: true }
    },
    {
        path: '/contracts',
        name: 'Contracts',
        component: () => import('@/views/dashboard/Contracts.vue'),
        meta: { requiresAuth: true }
    },
    {
        path: '/reports',
        name: 'Reports',
        component: () => import('@/views/dashboard/Reports.vue'),
        meta: { requiresAuth: true }
    }
]

const router = createRouter({
    history: createWebHistory(),
    routes
})

router.beforeEach((to, from, next) => {
    const isAuthenticated = localStorage.getItem('token');
    if (to.meta.requiresAuth && !isAuthenticated) {
        next('/login');
    } else {
        next();
    }
})

export default router
