<template>
  <v-app-bar color="primary" dark>
    <v-app-bar-title>Гостиница</v-app-bar-title>

    <v-spacer></v-spacer>

    <v-btn v-if="!isAuthenticated" to="/login" text>Вход</v-btn>
    <v-btn v-if="!isAuthenticated" to="/register" text>Регистрация</v-btn>

    <v-menu v-if="isAuthenticated" offset-y>
      <template v-slot:activator="{ props }">
        <v-btn v-bind="props" text>
          <v-icon left>mdi-account</v-icon>
          {{ user.username }}
        </v-btn>
      </template>

      <v-list>
        <v-list-item to="/profile">
          <v-list-item-title>Профиль</v-list-item-title>
        </v-list-item>
        <v-list-item to="/guests">
          <v-list-item-title>Гости</v-list-item-title>
        </v-list-item>
        <v-list-item to="/rooms">
          <v-list-item-title>Номера</v-list-item-title>
        </v-list-item>
        <v-list-item to="/bookings">
          <v-list-item-title>Бронирования</v-list-item-title>
        </v-list-item>
        <v-divider></v-divider>
        <v-list-item @click="handleLogout">
          <v-list-item-title>Выйти</v-list-item-title>
        </v-list-item>
      </v-list>
    </v-menu>
  </v-app-bar>
</template>

<script setup>
import { computed, ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const user = ref(JSON.parse(localStorage.getItem('user') || '{}'))

const isAuthenticated = computed(() => {
  return !!localStorage.getItem('auth_token')
})

const handleLogout = () => {
  // Удаляем токен и данные пользователя
  localStorage.removeItem('auth_token')
  localStorage.removeItem('user')

  // Перенаправляем на страницу входа
  router.push('/login')
}
</script>