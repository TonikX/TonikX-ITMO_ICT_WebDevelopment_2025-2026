<!-- components/AppBar.vue -->
<template>
  <v-app-bar
    color="primary"
    density="compact"
    elevation="1"
  >
    <v-app-bar-title @click="goHome">
        <v-icon start icon="mdi-car-back"></v-icon>
      <span class="font-weight-bold">CarRent</span>
    </v-app-bar-title>

    <v-spacer></v-spacer>

    <div v-if="!authStore.isAuthenticated">
      <v-btn
        to="/login"
        variant="text"
        color="white"
        class="mr-2"
      >
        <v-icon start icon="mdi-login"></v-icon>
        Войти
      </v-btn>
      <v-btn
        to="/register"
        variant="flat"
        color="white"
        class="text-primary"
      >
        <v-icon start icon="mdi-account-plus"></v-icon>
        Регистрация
      </v-btn>
    </div>

    <div v-else class="d-flex align-center">
      <v-btn
        to="/profile"
        variant="text"
        color="white"
        class="mr-2"
      >
        <v-icon start icon="mdi-account-circle"></v-icon>
        Профиль
      </v-btn>
      <v-btn
        @click="logout"
        variant="text"
        color="white"
      >
        <v-icon start icon="mdi-logout"></v-icon>
        Выйти
      </v-btn>
    </div>
  </v-app-bar>
</template>

<script setup>
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'

const authStore = useAuthStore()
const router = useRouter()

const logout = async () => {
  await authStore.logout();
  router.push('/login');
}

const goHome = () => {
  router.push('/');
};
</script>