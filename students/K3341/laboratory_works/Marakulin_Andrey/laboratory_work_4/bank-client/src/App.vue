<template>
  <v-app>
    <v-app-bar color="primary" density="compact">
      <v-app-bar-title>Банковская система</v-app-bar-title>

      <template v-if="authStore.isAuthenticated">
        <v-btn to="/clients">Клиенты</v-btn>
        <v-btn to="/passports">Паспорта</v-btn>
        <v-btn to="/deposits">Вклады</v-btn>
        <v-btn to="/credits">Кредиты</v-btn>
        <v-spacer></v-spacer>
        <v-btn icon="mdi-logout" @click="handleLogout" title="Выход"></v-btn>
      </template>

      <template v-else>
        <v-btn to="/login">Вход</v-btn>
        <v-btn to="/register">Регистрация</v-btn>
      </template>
    </v-app-bar>

    <v-main class="bg-grey-lighten-4">
      <v-container>
        <router-view></router-view>
      </v-container>
    </v-main>
  </v-app>
</template>

<script setup>
import { useAuthStore } from './stores/auth';
import { useRouter } from 'vue-router';

const authStore = useAuthStore();
const router = useRouter();

const handleLogout = () => {
  authStore.logout();
  router.push('/login');
};
</script>