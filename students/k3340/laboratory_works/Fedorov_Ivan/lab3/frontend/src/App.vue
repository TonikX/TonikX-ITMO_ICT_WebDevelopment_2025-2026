<!-- src/App.vue -->
<template>
  <v-app>
    <!-- Верхняя панель -->
    <v-app-bar elevation="1" class="px-4">
      <v-app-bar-title class="font-weight-bold">Hotel Admin</v-app-bar-title>

      <v-spacer />

      <!-- Навигация (desktop) -->
      <div class="d-none d-md-flex align-center ga-2">
        <v-btn variant="text" :to="nav.rooms" exact>НОМЕРА</v-btn>
        <v-btn variant="text" :to="nav.clients">КЛИЕНТЫ</v-btn>
        <v-btn variant="text" :to="nav.employees">СОТРУДНИКИ</v-btn>
        <v-btn variant="text" :to="nav.cleaning">УБОРКА</v-btn>
        <v-btn variant="text" :to="nav.report">ОТЧЁТ</v-btn>
        <v-btn variant="text" :to="nav.stats">СТАТИСТИКА</v-btn>
      </div>

      <!-- Меню (mobile) -->
      <v-menu class="d-md-none">
        <template #activator="{ props }">
          <v-btn icon="mdi-menu" v-bind="props" />
        </template>
        <v-list density="compact">
          <v-list-item :to="nav.rooms" title="Номера" />
          <v-list-item :to="nav.clients" title="Клиенты" />
          <v-list-item :to="nav.employees" title="Сотрудники" />
          <v-list-item :to="nav.cleaning" title="Уборка" />
          <v-list-item :to="nav.report" title="Отчёт" />
          <v-list-item :to="nav.stats" title="Статистика" />
        </v-list>
      </v-menu>

      <v-divider vertical class="mx-3 d-none d-md-flex" />

      <v-btn color="red" variant="flat" @click="doLogout">ВЫЙТИ</v-btn>
    </v-app-bar>

    <!-- Контент -->
    <v-main class="main">
      <v-container class="content">
        <router-view />
      </v-container>
    </v-main>
  </v-app>
</template>

<script setup>
import { useRouter } from "vue-router";
import { logout } from "./services/auth";

const router = useRouter();

const nav = {
  rooms: "/rooms",
  clients: "/clients",
  employees: "/employees",
  cleaning: "/cleaning",
  report: "/report",
  stats: "/stats",
};

function doLogout() {
  logout();
  router.push("/login");
}
</script>

<style scoped>
.main {
  padding-top: 46px;
}
.content {
  max-width: 1200px;
}
</style>
