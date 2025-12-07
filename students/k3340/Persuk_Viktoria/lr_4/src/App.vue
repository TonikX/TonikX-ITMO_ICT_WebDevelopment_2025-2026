<template>
  <v-app>
    <v-app-bar color="primary" prominent dark>
      <v-app-bar-nav-icon
        v-if="$vuetify.display.mobile"
        @click="drawer = !drawer"
      ></v-app-bar-nav-icon>

      <v-toolbar-title>
        <router-link to="/" class="text-white text-decoration-none">
          Drones App
        </router-link>
      </v-toolbar-title>

      <v-spacer></v-spacer>

      <!-- Навигация для авторизованных -->
      <template v-if="authStore.isAuthenticated">
        <v-btn to="/" variant="text" class="mr-2">Главная</v-btn>
        <v-btn to="/drones" variant="text" class="mr-2">Дроны</v-btn>
        <v-btn to="/flights" variant="text" class="mr-2">Полёты</v-btn>
        <v-btn variant="text" @click="handleLogout">Выход</v-btn>
      </template>

      <!-- Навигация для гостей -->
      <template v-else>
        <v-btn to="/login" variant="text" class="mr-2">Вход</v-btn>
        <v-btn to="/register" variant="outlined">Регистрация</v-btn>
      </template>
    </v-app-bar>

    <v-navigation-drawer v-model="drawer" temporary v-if="$vuetify.display.mobile">
      <v-list>
        <template v-if="authStore.isAuthenticated">
          <v-list-item prepend-icon="mdi-view-dashboard" title="Главная" to="/"></v-list-item>
          <v-list-item prepend-icon="mdi-airplane" title="Дроны" to="/drones"></v-list-item>
          <v-list-item prepend-icon="mdi-flight-takeoff" title="Полёты" to="/flights"></v-list-item>
          <v-list-item prepend-icon="mdi-logout" title="Выход" @click="handleLogout"></v-list-item>
        </template>
        <template v-else>
          <v-list-item prepend-icon="mdi-login" title="Вход" to="/login"></v-list-item>
          <v-list-item prepend-icon="mdi-account-plus" title="Регистрация" to="/register"></v-list-item>
        </template>
      </v-list>
    </v-navigation-drawer>

    <v-main>
      <v-container fluid>
        <router-view />
      </v-container>
    </v-main>

    <!-- Snackbar для уведомлений -->
    <v-snackbar v-model="snackbar.show" :color="snackbar.color" :timeout="snackbar.timeout" location="top">
      {{ snackbar.message }}
      <template v-slot:actions>
        <v-btn variant="text" @click="snackbar.show = false">Закрыть</v-btn>
      </template>
    </v-snackbar>
  </v-app>
</template>

<script setup>
import { ref, provide } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/authStore'

const router = useRouter()
const authStore = useAuthStore()

const drawer = ref(false)

const snackbar = ref({
  show: false,
  message: '',
  color: 'success',
  timeout: 5000,
})

const showSnackbar = (message, color = 'success', timeout = 5000) => {
  snackbar.value = { show: true, message, color, timeout }
}

provide('showSnackbar', showSnackbar)

const handleLogout = async () => {
  await authStore.logout()
  router.push('/login')
  showSnackbar('Вы вышли из системы', 'info')
}
</script>

<style scoped>
.text-white {
  color: white !important;
}
</style>
