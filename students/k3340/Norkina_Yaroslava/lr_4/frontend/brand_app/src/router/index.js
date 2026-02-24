import { createRouter, createWebHistory } from 'vue-router'
import store from '../store'

// Импортируем все страницы
import HomeView from '../views/HomeView.vue'
import LoginView from '../views/LoginView.vue'
import RegisterView from '../views/RegisterView.vue'
import ServicesView from '../views/ServicesView.vue'
import ProfileView from '../views/ProfileView.vue'
import ServiceDetailView from '../views/ServiceDetailView.vue'
import CreateOrderView from '../views/CreateOrderView.vue'
import AdminServicesView from '../views/AdminServicesView.vue'
import AdminServiceDetailView from '../views/AdminServiceDetailView.vue'
import AdminServiceEditView from '../views/AdminServiceEditView.vue'
import AdminOrdersView from '../views/AdminOrdersView.vue'
import AdminReviewsView from '../views/AdminReviewsView.vue'
import OrdersView from '../views/OrdersView.vue'

const routes = [
    {
        path: '/',
        name: 'Home',
        component: HomeView
    },
    {
        path: '/services',
        name: 'Services',
        component: ServicesView
    },
    {
        path: '/login',
        name: 'Login',
        component: LoginView,
        meta: { guestOnly: true }
    },
    {
        path: '/register',
        name: 'Register',
        component: RegisterView,
        meta: { guestOnly: true }
    },
    {
        path: '/profile',
        name: 'Profile',
        component: ProfileView,
        meta: { requiresAuth: true }
    },
    {
        path: '/services/:id',
        name: 'ServiceDetail',
        component: ServiceDetailView,
        meta: { title: 'Детали услуги' }
    },
    {
        path: '/orders/new',
        name: 'CreateOrder',
        component: CreateOrderView,
        meta: {
            title: 'Новая заявка',
            requiresAuth: true
        }
    },
    {
        path: '/admin/services',
        name: 'AdminServices',
        component: AdminServicesView,
        meta: {
            title: 'Управление услугами',
            requiresAuth: true,
            requiresAdmin: true
        }
    },
    {
        path: '/admin/services/new',
        name: 'AdminServiceCreate',
        component: AdminServiceEditView,
        meta: {
            title: 'Новая услуга',
            requiresAuth: true,
            requiresAdmin: true
        }
    },
    {
        path: '/admin/services/:id',
        name: 'AdminServiceDetail',
        component: AdminServiceDetailView,
        meta: {
            title: 'Детали услуги',
            requiresAuth: true,
            requiresAdmin: true
        }
    },
    {
        path: '/admin/services/:id/edit',
        name: 'AdminServiceEdit',
        component: AdminServiceEditView,
        meta: {
            title: 'Редактирование услуги',
            requiresAuth: true,
            requiresAdmin: true
        }
    },
    {
        path: '/admin/orders',
        name: 'AdminOrders',
        component: AdminOrdersView
    },
    {
        path: '/admin/reviews',
        name: 'AdminReviews',
        component: AdminReviewsView
    },
    {
        path: '/orders',
        name: 'Orders',
        component: OrdersView
    }
]

const router = createRouter({
    history: createWebHistory(),
    routes
})

// Навигационная охрана
router.beforeEach((to, from, next) => {
    const isAuthenticated = store.state.auth.token
    const user = store.state.auth.user
    const isAdmin = user?.role === 'admin' || user?.is_staff === true

    // Если маршрут только для гостей
    if (to.meta.guestOnly && isAuthenticated) {
        next('/')
        return
    }

    // Если маршрут требует авторизации
    if (to.meta.requiresAuth && !isAuthenticated) {
        next('/login')
        return
    }

    // Если маршрут требует админских прав
    if (to.meta.requiresAdmin && (!isAuthenticated || !isAdmin)) {
        next('/')
        return
    }

    next()
})

export default router