<template>
  <v-app>
    <v-app-bar color="deep-purple-accent-4" elevation="4">
      <v-app-bar-title>
        <span class="logo-dot">•</span>
        stay easy hotel
      </v-app-bar-title>
      <v-spacer></v-spacer>
      <v-btn variant="text" to="/rooms">номера</v-btn>
      <v-btn variant="text" to="/my-bookings" v-if="isAuth">мои брони</v-btn>
      <v-btn variant="text" to="/login" v-if="!isAuth">войти</v-btn>
      <v-btn variant="text" @click="logout" v-else>выйти</v-btn>
    </v-app-bar>

    <v-main class="app-main">
      <v-container class="py-6">
        <router-view />
      </v-container>
    </v-main>
  </v-app>
</template>

<script setup>
import { computed } from 'vue'
import { useAuthStore } from './store/auth'
import { useRouter } from 'vue-router'

// простой доступ к состоянию авторизации
const auth = useAuthStore()
const router = useRouter()

const isAuth = computed(() => !!auth.token.value)

const logout = async () => {
  // выход из системы и возврат на страницу логина
  await auth.logout()
  router.push('/login')
}
</script>

<style scoped>
.app-main {
  /* простой градиентный фон*/
  background: radial-gradient(circle at top left, #ede7f6, #ffffff);
}

.logo-dot {
  color: #ffd54f;
  font-size: 26px;
  margin-right: 4px;
}
</style>

