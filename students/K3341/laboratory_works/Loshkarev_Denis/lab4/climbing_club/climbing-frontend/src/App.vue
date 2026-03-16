<template>
  <v-app>
    <v-app-bar color="blue-darken-3" dark>
      <v-app-bar-title>АльпКлуб Админ</v-app-bar-title>
      <v-spacer></v-spacer>
      
      <v-btn to="/mountains" text v-if="auth.token">Вершины</v-btn>

      <v-btn to="/login" text v-if="!auth.token">Войти</v-btn>
      <v-btn @click="logout" text v-else prepend-icon="mdi-logout">Выйти</v-btn>
    </v-app-bar>
    <v-main>
      <router-view></router-view>
    </v-main>
  </v-app>
</template>

<script setup>
import { useAuthStore } from './stores/auth'
import { useRouter } from 'vue-router'

const auth = useAuthStore()
const router = useRouter()

const logout = () => {
  auth.logout()
  router.push('/login')
}
</script>
