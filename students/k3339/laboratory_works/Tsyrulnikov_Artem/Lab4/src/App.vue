<template>
  <v-app>
    <v-app-bar v-if="auth.isAuth" color="primary">
      <v-app-bar-title>Рекламное агентство</v-app-bar-title>
      <v-btn to="/">Главная</v-btn>
      <v-btn to="/clients">Клиенты</v-btn>
      <v-btn to="/services">Услуги</v-btn>
      <v-btn to="/orders">Заказы</v-btn>
      <v-btn to="/payments">Платежи</v-btn>
      <v-btn to="/profile">Профиль</v-btn>
      <v-btn @click="logout">Выход</v-btn>
    </v-app-bar>
    <v-main>
      <v-container>
        <router-view />
      </v-container>
    </v-main>
  </v-app>
</template>

<script setup>
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'

const auth = useAuthStore()
const router = useRouter()

const logout = () => {
  auth.logout()
  router.push('/login')
}
</script>
