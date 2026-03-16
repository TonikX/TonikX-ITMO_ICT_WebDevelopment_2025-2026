import {createRouter, createWebHistory} from "vue-router";

const routes = [
    {
        path: '/auth',
        component: () => import("@/views/AuthPage.vue")
    },
    {
        path: '/login',
        component: () => import("@/views/LoginPage.vue")
    },
    {
        path: '/signup',
        component: () => import("@/views/SignUpPage.vue"),
    },
    {
        path: '/main',
        component: () => import("@/views/MainPage.vue")
    },
    {
        path: '/list/:type',
        name: 'ListPage',
        component: () => import('@/views/ListPage.vue'),
        props: true
    },
    {
        path: '/list/:type/:id',
        name: 'ItemPage',
        component: () => import('@/views/ItemPage.vue'),
        props: true
    },
    {
        path: '/list/:type/add',
        name: 'AddPage',
        component: () => import('@/views/AddPage.vue'),
        props: true
    },
    {
        path: '/list/:type/:id/edit',
        name: 'EditPage',
        component: () => import('@/views/EditPage.vue'),
        props: true
    },
    {
        path: '/profile',
        name: 'ProfilePage',
        component: () => import('@/views/ProfilePage.vue'),
    },
    {
        path: '/',
        component: () => import('@/views/RootRedirect.vue')
    }
]

const router = createRouter({
   history: createWebHistory(), routes
})

export default router
