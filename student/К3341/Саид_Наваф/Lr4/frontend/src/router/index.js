import { createRouter, createWebHistory } from "vue-router";
import Home from "@/views/HomeView.vue";
import Owners from "@/views/Owners.vue";
import OwnerDetail from "@/views/OwnerDetail.vue";
import OwnerEdit from "@/views/OwnerEdit.vue";
import Cars from "@/views/Cars.vue";
import CarDetail from "@/views/CarsDetail.vue";
import VehicleModels from "@/views/VehicleModels.vue";

const routes = [
  { path: "/", name: "Home", component: Home },
  { path: "/owners", name: "Owners", component: Owners },
  { path: "/owners/:id", name: "OwnerDetail", component: OwnerDetail, props: true },
  { path: "/owners/:id/edit", name: "OwnerEdit", component: OwnerEdit, props: true },
  { path: "/cars", name: "Cars", component: Cars },
  { path: "/cars/:id", name: "CarDetail", component: CarDetail, props: true },
  { path: "/vehicle-models", name: "VehicleModels", component: VehicleModels },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;