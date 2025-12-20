import { createRouter, createWebHistory } from 'vue-router';
import FlightList from '../components/FlightList.vue';
import CrewDetails from '../components/CrewDetails.vue';
import RouteDetails from '../components/RouteDetails.vue';
import RoutesList from '../components/RoutesList.vue';
import FlightDetails from '../components/FlightDetails.vue';
import AirlineCompanyList from '../components/AirLineCompanyList.vue';
import CreateCompany from '../components/CreateCompany.vue';
import CreateCrew from '../components/CreateCrew.vue';
import CreateCrewMember from '../components/CreateCrewMember.vue';
import CreateFlight from '../components/CreateFlight.vue';
import CreatePlane from '../components/CreatePlane.vue';
import CreateRoute from '../components/CreateRoute.vue';
import EditRoute from '@/components/EditRoute.vue';
import EditFlight from '../components/EditFlight.vue';
import EditCompany from '@/components/EditCompany.vue';
import PlaneList from '@/components/PlaneList.vue';
import EditPlane from '@/components/EditPlane.vue';
import CrewList from '../components/CrewList.vue';
import EditCrew from '../components/EditCrew.vue';
import EditCrewMember from '../components/EditCrewMember.vue';
import Register from '@/components/Register.vue';
import Login from '@/components/Login.vue';
import Profile from '@/components/Profile.vue';
import VariantTask from '@/components/VariantTask.vue';

const EmptyPage = { template: '<div style="padding: 20px;">Страница создания объекта</div>' };

const routes = [
  {
    path: '/flights',
    name: 'Flights',
    component: FlightList,
  },
  {
    path: '/crews/:id',
    name: 'CrewDetails',
    component: CrewDetails,
    props: true,
  },
  {
    path: '/routes',
    name: 'RoutesList',
    component: RoutesList,
  },
  {
    path: '/route/:id',
    name: 'RouteDetails',
    component: RouteDetails,
    props: true,
  },
  {
    path: '/flight/:id',
    name: 'FlightDetails',
    component: FlightDetails,
    props: true,
  },
  {
    path: '/airlines',
    name: 'AirlineCompanyList',
    component: AirlineCompanyList,
  },
  {
    path: '/edit-company/:id',
    component: EditCompany,
    name: 'EditCompany',
  },
  {
    path: '/create-plane',
    name: 'CreatePlane',
    component: CreatePlane,
  },
  {
    path: '/create-company',
    name: 'CreateCompany',
    component: CreateCompany,
  },
  {
    path: '/create-route',
    name: 'CreateRoute',
    component: CreateRoute,
  },
  {
    path: '/create-crew-member',
    name: 'CreateCrewMember',
    component: CreateCrewMember,
  },
  {
    path: '/create-crew',
    name: 'CreateCrew',
    component: CreateCrew,
  },
  {
    path: '/create-flight',
    name: 'CreateFlight',
    component: CreateFlight,
  },
  {
    path: '/routes',
    component: RoutesList,
    name: 'RoutesList',
  },
  {
    path: '/edit-route/:id',
    component: EditRoute,
    name: 'EditRoute',
  },
  {
    path: '/flights',
    component: FlightList,
    name: 'FlightList',
  },
  {
    path: '/edit-flight/:id',
    component: EditFlight,
    name: 'EditFlight',
  },
  {
    path: '/planes',
    name: 'PlaneList',
    component: PlaneList,
  },
  {
    path: '/edit-plane/:id',
    name: 'EditPlane',
    component: EditPlane,
    props: true,
  },
    {
    path: '/crews',
    name: 'CrewList',
    component: CrewList,
  },
  {
    path: '/edit-crew/:id',
    name: 'EditCrew',
    component: EditCrew,
    props: true,
  },
  {
    path: '/edit-crew-member/:id',
    name: 'EditCrewMember',
    component: EditCrewMember,
    props: true,
  },
  {
    path: "/register",
    name: "Register",
    component: Register,
  },
  {
    path: "/login",
    name: "Login",
    component: Login,
  },
  {
    path: "/profile",
    name: "Profile",
    component: Profile,
  },
  {
    path: '/variant-task',
    name: 'VariantTask',
    component: VariantTask,
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;