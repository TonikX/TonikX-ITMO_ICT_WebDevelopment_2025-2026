import { createRouter, createWebHistory } from 'vue-router'
import store from '../store'
import AdminMaintenanceCompanyList from '@/views/admin/maintenance/AdminMaintenanceCompanyList.vue'
import AdminMaintenanceCompanyForm from '@/views/admin/maintenance/AdminMaintenanceCompanyForm.vue'
import AdminMaintenanceCompanyDetail from '@/views/admin/maintenance/AdminMaintenanceCompanyDetail.vue'
import CarMaintenance from "@/views/admin/cars/CarMaintenance.vue"

const routes = [
    {
        path: '/',
        name: 'Home',
        component: () => import('../views/Home.vue'),
        meta: { requiresAuth: true }
    },
    {
        path: '/login',
        name: 'Login',
        component: () => import('../views/Login.vue'),
        meta: { guestOnly: true }
    },
    {
        path: '/profile',
        name: 'Profile',
        component: () => import('../views/Profile.vue'),
        meta: { requiresAuth: true }
    },
    {
        path: '/register',
        name: 'Register',
        component: () => import('../views/Register.vue'),
        meta: { guestOnly: true }
    },

    // === СТРАНИЦЫ ДЛЯ КЛИЕНТОВ ===
    {
        path: '/cars',
        name: 'CarsList',
        component: () => import('../views/cars/CarsList.vue'),
        meta: { requiresAuth: true }
    },
    {
        path: '/cars/:id',
        name: 'CarDetail',
        component: () => import('../views/cars/CarDetail.vue'),
        meta: { requiresAuth: true },
        props: true
    },
    {
        path: '/cars/:id/application',
        name: 'CarApplication',
        component: () => import('../views/cars/CarApplication.vue'),
        meta: { requiresAuth: true },
        props: true
    },


    // === АДМИН ПАНЕЛЬ ===
    {
        path: '/admin',
        component: () => import('../views/admin/AdminLayout.vue'),
        meta: { requiresAuth: true, requiresAdmin: true },
        children: [
            {
                path: '',
                name: 'AdminDashboard',
                component: () => import('../views/admin/Dashboard.vue')
            },
            // Автомобили
            {
                path: 'cars',
                name: 'AdminCars',
                component: () => import('../views/admin/cars/AdminCarList.vue')
            },
            {
                path: 'cars/new',
                name: 'AdminCarCreate',
                component: () => import('../views/admin/cars/AdminCarForm.vue')
            },
            {
                path: 'cars/:id/edit',
                name: 'AdminCarEdit',
                component: () => import('../views/admin/cars/AdminCarForm.vue'),
                props: true
            },
            {
                path: 'cars/:id',
                name: 'AdminCarDetail',
                component: () => import('../views/admin/cars/AdminCarDetail.vue'),
                props: true
            },
            {
                path: 'cars/:id/specifications',
                name: 'CarSpecificationDetail',
                component: () => import('@/views/admin/cars/CarSpecificationDetail.vue'),
                props: true
            },
            {
                path: 'cars/:id/specifications/create',
                name: 'CarSpecificationCreate',
                component: () => import('@/views/admin/cars/CarSpecificationForm.vue'),
                props: true
            },
            {
                path: 'cars/:id/maintenance',
                name: 'CarMaintenance',
                component: CarMaintenance,
                props: true
            },
            // Заявки
            {
                path: 'applications',
                name: 'AdminApplications',
                component: () => import('../views/admin/applications/AdminApplicationList.vue')
            },
            {
                path: 'applications/:id',
                name: 'AdminApplicationDetail',
                component: () => import('../views/admin/applications/AdminApplicationDetail.vue'),
                props: true
            },
            // Договоры
            {
                path: 'leases',
                name: 'AdminLeases',
                component: () => import('../views/admin/leases/AdminLeaseList.vue')
            },
            {
                path: 'leases/:id',
                name: 'AdminLeaseDetail',
                component: () => import('../views/admin/leases/AdminLeaseDetail.vue'),
                props: true
            },
            // Клиенты
            {
                path: 'clients',
                name: 'AdminClients',
                component: () => import('../views/admin/clients/AdminClientList.vue')
            },
            {
                path: 'cars/:id/leasings',
                name: 'AdminCarLeasings',
                component: () => import('../views/admin/cars/CarLeasings.vue'),
                props: true
            },
            {
                path: 'clients/:id',
                name: 'AdminClientDetail',
                component: () => import('../views/admin/clients/AdminClientDetail.vue'),
                props: true
            },
            {
                path: 'reports',
                name: 'AdminReports',
                component: () => import('../views/admin/AdminReports.vue')
            },
            {
                path: 'maintenance_companies',
                name: 'AdminMaintenanceCompanyList',
                component: AdminMaintenanceCompanyList
            },
            {
                path: 'maintenance_companies/new',
                name: 'AdminMaintenanceCompanyCreate',
                component: AdminMaintenanceCompanyForm
            },
            {
                path: 'maintenance_companies/:id',
                name: 'AdminMaintenanceCompanyDetail',
                component: AdminMaintenanceCompanyDetail,
                props: true
            },
            {
                path: 'maintenance_companies/:id/edit',
                name: 'AdminMaintenanceCompanyEdit',
                component: AdminMaintenanceCompanyForm,
                props: true
            },
        ]
    }
]

const router = createRouter({
    history: createWebHistory(),
    routes
})

// Навигационный guard
router.beforeEach((to, from, next) => {
    const isAuthenticated = store.getters['auth/isAuthenticated']
    const isAdmin = store.getters['auth/user']?.is_staff || false

    // Если маршрут требует авторизации
    if (to.matched.some(record => record.meta.requiresAuth) && !isAuthenticated) {
        next('/login')
    }
    // Если маршрут требует прав администратора
    else if (to.matched.some(record => record.meta.requiresAdmin) && !isAdmin) {
        next('/')
    }
    // Если маршрут только для гостей, а пользователь авторизован
    else if (to.matched.some(record => record.meta.guestOnly) && isAuthenticated) {
        next('/')
    }
    else {
        next()
    }
})


export default router