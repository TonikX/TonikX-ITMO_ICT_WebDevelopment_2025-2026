import {createRouter, createWebHistory} from "vue-router";
import LoginView from "@/views/auth/LoginView.vue";
import RegisterView from "@/views/auth/RegisterView.vue";
import {tokenStore} from "@/stores/token.js";
import AgentsView from "@/views/agents/AgentsView.vue";
import AgentsDetailView from "@/views/agents/AgentsDetailView.vue";
import ReportView from "@/views/ReportView.vue";
import OrganizationView from "@/views/organizations/OrganizationView.vue";
import OrganizationDetailView from "@/views/organizations/OrganizationDetailView.vue";
import ClientsView from "@/views/clients/ClientsView.vue";
import ClientsDetailView from "@/views/clients/ClientsDetailView.vue";


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
        path: '/agents',
        component: AgentsView
    },
    {
      path: '/agents/:id',
      component: AgentsDetailView
    },
    {
        path: '/organizations',
        component: OrganizationView
    },
    {
        path: '/organizations/:id',
        component: OrganizationDetailView
    },
    {
        path: '/clients',
        component: ClientsView
    },
    {
        path: '/clients/:id',
        component: ClientsDetailView
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
