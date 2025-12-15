import { createRouter, createWebHistory } from 'vue-router';
import FlightList from '../components/FlightList.vue';
import CrewDetails from '../components/CrewDetails.vue';
import RouteDetails from '../components/RouteDetails.vue';
import RoutesList from '../components/RoutesList.vue';
import FlightDetails from '../components/FlightDetails.vue';

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
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;