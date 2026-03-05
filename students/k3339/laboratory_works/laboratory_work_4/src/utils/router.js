import {createRouter, createWebHistory} from "vue-router";
import LoginView from "@/views/auth/LoginView.vue";
import RegisterView from "@/views/auth/RegisterView.vue";
import {tokenStore} from "@/stores/token.js";
import EmployeeView from "@/views/employee/EmployeeView.vue";
import EmployeeDetailView from "@/views/employee/EmployeeDetailView.vue";
import ChickenView from "@/views/chicken/ChickenView.vue";
import ChickenDetailView from "@/views/chicken/ChickenDetailView.vue";
import ReportView from "@/views/ReportView.vue";
import CellView from "@/views/cell/CellView.vue";
import CellDetailView from "@/views/cell/CellDetailView.vue";


const routes = [
    {
        name: 'Login',
        path: '/login',
        component: LoginView
    },
    {
        name: 'Register',
        path: '/register',
        component: RegisterView
    },
    {
        path: '/employees',
        component: EmployeeView
    },
    {
      path: '/employees/:id',
      component: EmployeeDetailView
    },
    {
        path: '/chickens',
        component: ChickenView
    },
    {
        path: '/chickens/:id',
        component: ChickenDetailView
    },
    {
        path: '/cells',
        component: CellView
    },
    {
        path: '/cells/:id',
        component: CellDetailView
    },
    {
        path: '/reports',
        component: ReportView
    }
]

const router = createRouter({
    history: createWebHistory(), routes
})

export default router

router.beforeEach((to, from, next) => {
    const token = tokenStore().token;

    if (to.name !== 'Login' && to.name !== 'Register' && !token) {
        next({name: 'Login'});
    } else {
        next();
    }
});
